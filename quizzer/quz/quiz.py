class QuizDataError(Exception):
    pass


def _create_data_dict(marked_user_input: str) -> dict:
    text_lines = marked_user_input.strip().split('\n')
    if len(text_lines) < 3:
        raise QuizDataError('Invalid text; line count < 3 - min is 1 question and two options')
    data_dict = {'latest_question_num': 1, 'num_of_completed_questions': 0, 'marked_user_input': marked_user_input}
    num_of_answers = 0
    num_of_questions = 0
    question_answers = {}
    question_text = None
    comment = None

    for i, line in enumerate(text_lines):
        line = line.strip()
        if len(line) == 0:
            continue

        if line.startswith('?'):
            if num_of_questions != 0:
                _add_question_to_data_dict(comment, num_of_answers, num_of_questions, question_answers, question_text,
                                           data_dict)
            question_text = line[1:]
            num_of_questions += 1

            num_of_answers = 0
            question_answers = {}
            comment = None
        elif line.startswith('+') or line.startswith('-'):
            num_of_answers += 1
            answer = {'is_correct': line.startswith('+'), 'is_selected': False, 'answer': line[1:]}
            question_answers['answer' + str(num_of_answers)] = answer
        elif line.startswith('='):
            if comment is not None:
                raise QuizDataError(f'More than one comment for question;  line#{i}; line={line}')
            comment = line[1:]
        else:
            raise QuizDataError(f'First character is not: ?+-=  line#{i}; line={line}')

    _add_question_to_data_dict(comment, num_of_answers, num_of_questions, question_answers, question_text, data_dict)
    data_dict['num_of_questions'] = num_of_questions
    return data_dict


def _add_question_to_data_dict(comment: str, num_of_answers: int, num_of_questions: int, question_answers: dict,
                               question_text: str, data_dict: dict):
    question_answers['num_of_answers'] = num_of_answers
    if comment is not None:
        question_answers['comment'] = comment
    data_dict['question' + str(num_of_questions)] = question_text
    data_dict['question' + str(num_of_questions) + '_answers'] = question_answers


class Quiz(dict):
    def __init__(self, marked_user_input: str = None, quiz_data: dict = None):
        if quiz_data is None:
            quiz_data = _create_data_dict(marked_user_input)
        self._current_question_num = 1
        super(Quiz, self).__init__(quiz_data)

        self._initial_len = len(self.keys())

    @property
    def quiz_file_path(self) -> str:
        return self._quiz_file_path

    def marked_user_input(self) -> str:
        return self['marked_user_input']

    def next_question(self) -> tuple:
        if self._current_question_num < self['num_of_questions']:
            self._current_question_num += 1
        return self._question_and_answers(self._current_question_num)

    def current_question(self) -> tuple:
        return self._question_and_answers(self._current_question_num)

    def previous_question(self) -> tuple:
        if self._current_question_num > 1:
            self._current_question_num -= 1
        return self._question_and_answers(self._current_question_num)

    def _question_and_answers(self, question_num) -> tuple:
        key = 'question' + str(question_num)
        key2 = key + '_answers'
        return self[key], self[key2]

    def score(self) -> tuple:
        num_of_incorrect_questions = 0
        num_of_questions = self['num_of_questions']
        for i in range(1, num_of_questions + 1):
            _, question_answers = self._question_and_answers(i)
            for j in range(1, question_answers['num_of_answers'] + 1):
                key = 'answer' + str(j)
                answer = question_answers[key]
                if (answer['is_correct'] and not answer['is_selected']) or \
                        (not answer['is_correct'] and answer['is_selected']):
                    num_of_incorrect_questions += 1
                    break
        ratio = f'{num_of_questions - num_of_incorrect_questions}/{num_of_questions}'
        percent = round(100. * (num_of_questions - num_of_incorrect_questions) / num_of_questions)
        return ratio, f'{percent}%'
