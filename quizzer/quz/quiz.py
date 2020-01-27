import logging
from typing import List


class QuizDataError(Exception):
    pass


class MultipleChoiceAnswer:
    def __init__(self, answer: str, is_correct: bool, is_selected: bool):
        self._answer = answer
        self._is_correct = is_correct
        self._is_selected = is_selected
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(self.__repr__())

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def is_correct(self) -> bool:
        return self._is_correct

    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        self._is_selected = value

    def is_selected_correct(self):
        return (self._is_selected and self._is_correct) or \
               (not self._is_selected and not self._is_correct)

    def __eq__(self, other) -> bool:
        if isinstance(other, MultipleChoiceAnswer):
            return self.answer == other.answer and \
                   self.is_correct == other.is_correct and \
                   self.is_selected == other.is_selected
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f'MultipleChoiceAnswer("{self.answer}", {self.is_correct}, {self.is_selected})'


class MultipleChoiceQuestion:
    def __init__(self, question: str, comment: str or None, answers: List[MultipleChoiceAnswer]):
        self._question = question
        self._comment = comment
        self._answers = answers
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(self.__repr__())

    @property
    def question(self) -> str:
        return self._question

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def answers(self) -> List[MultipleChoiceAnswer]:
        return self._answers

    def are_answers_correct(self) -> bool:
        for answer in self._answers:
            if not answer.is_selected_correct():
                return False
        return True

    def is_answered(self) -> bool:
        for answer in self._answers:
            if answer.is_selected:
                return True
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, MultipleChoiceQuestion):
            return self.question == other.question and \
                   self.comment == other.comment and \
                   self.answers == other.answers
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        text = self.comment
        if text is not None:
            text = '"' + text + '"'
        return f'MultipleChoiceQuestion("{self.question}", {text}, {self.answers})'


def _create_quiz_data_dict(marked_user_input: str) -> dict:
    text_lines = marked_user_input.strip().split('\n')
    if len(text_lines) < 3:
        raise QuizDataError('Invalid text; line count < 3 - min is 1 question and two options')
    quiz_data_dict = {'current_question_num': 1, 'marked_user_input': marked_user_input}
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
                _add_question_to_quiz_data_dict(comment, num_of_answers, num_of_questions, question_answers,
                                                question_text, quiz_data_dict)
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
        elif line.startswith('/'):
            pass
        else:
            raise QuizDataError(f'First character is not: ?+-=/  line#{i}; line={line}')

    _add_question_to_quiz_data_dict(comment, num_of_answers, num_of_questions, question_answers, question_text,
                                    quiz_data_dict)
    quiz_data_dict['num_of_questions'] = num_of_questions
    return quiz_data_dict


def _add_question_to_quiz_data_dict(comment: str, num_of_answers: int, num_of_questions: int, question_answers: dict,
                                    question_text: str, quiz_data_dict: dict):
    question_answers['num_of_answers'] = num_of_answers
    if comment is not None:
        question_answers['comment'] = comment
    quiz_data_dict['question' + str(num_of_questions)] = question_text
    quiz_data_dict['question' + str(num_of_questions) + '_answers'] = question_answers


class Quiz:
    def __init__(self, marked_user_input: str = None, quiz_data_dict: dict = None):
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                f' marked_user_input={marked_user_input}\nquiz_data_dict={quiz_data_dict}')
        if quiz_data_dict is None and marked_user_input is None:
            raise ValueError(f'marked_user_input and quiz_data_dict are both none')
        elif quiz_data_dict is not None and marked_user_input is not None:
            raise ValueError(f'marked_user_input or quiz_data_dict must be none')

        if quiz_data_dict is None:
            self._quiz_data_dict = _create_quiz_data_dict(marked_user_input)
        else:
            self._quiz_data_dict = quiz_data_dict
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'quiz_data_dict={self._quiz_data_dict}')
        self._questions = _create_questions(self._quiz_data_dict)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'questions={self.questions}')

        self._current_question_num = self._quiz_data_dict['current_question_num']
        self._marked_user_input = self._quiz_data_dict['marked_user_input']
        self._num_of_questions = self._quiz_data_dict['num_of_questions']

    @property
    def num_of_questions(self) -> int:
        return self._num_of_questions

    @property
    def marked_user_input(self) -> str:
        return self._marked_user_input

    @property
    def questions(self) -> List[MultipleChoiceQuestion]:
        return self._questions

    @property
    def current_question_num(self) -> int:
        return self._current_question_num

    def next_question(self) -> MultipleChoiceQuestion:
        if self._current_question_num < len(self._questions):
            self._current_question_num += 1
        return self.current_question()

    def current_question(self) -> MultipleChoiceQuestion:
        return self._questions[self._current_question_num - 1]

    def previous_question(self) -> MultipleChoiceQuestion:
        if self._current_question_num > 1:
            self._current_question_num -= 1
        return self.current_question()

    def set_selected_of_current_question(self, answer_num: int, is_selected: bool) -> None:
        current_question: MultipleChoiceQuestion = self._questions[self._current_question_num - 1]
        answer: MultipleChoiceAnswer = current_question.answers[answer_num]
        answer.is_selected = is_selected

    def score(self) -> tuple:
        num_of_correct_questions = 0
        num_of_questions = len(self._questions)
        for question in self._questions:
            if question.are_answers_correct():
                num_of_correct_questions += 1
        ratio = f'{num_of_correct_questions}/{num_of_questions}'
        percent = round(100. * num_of_correct_questions / num_of_questions)
        return ratio, f'{percent}%'

    def data_dict(self) -> dict:
        data_dict = {'current_question_num': self.current_question_num,
                     'num_of_questions': self.num_of_questions,
                     'marked_user_input': self.marked_user_input}
        for i in range(self.num_of_questions):
            question: MultipleChoiceQuestion = self.questions[i]
            key_i = 'question' + str(i + 1)
            data_dict[key_i] = question.question
            question_answers_dict = dict()
            for j in range(len(question.answers)):
                answer: MultipleChoiceAnswer = question.answers[j]
                answer_dict = {'answer': answer.answer, 'is_correct': answer.is_correct,
                               'is_selected': answer.is_selected}
                key_j = 'answer' + str(j + 1)
                question_answers_dict[key_j] = answer_dict
            question_answers_dict['comment'] = question.comment
            question_answers_dict['num_of_answers'] = len(question.answers)
            key = key_i + '_answers'
            data_dict[key] = question_answers_dict
        return data_dict

    def __repr__(self) -> str:
        return f'Quiz(current_question_num={self._current_question_num}, num_of_questions=' \
               f'{self.num_of_questions}, {self._questions})'


def _create_questions(_quiz_data_dict: dict) -> List[MultipleChoiceQuestion]:
    num_of_questions = _quiz_data_dict['num_of_questions']
    questions = []
    for i in range(1, num_of_questions + 1):
        key = 'question' + str(i)
        question_text = _quiz_data_dict[key]
        key2 = key + '_answers'
        answers_dict = _quiz_data_dict[key2]
        comment = answers_dict.get('comment')
        answers = _create_answers(answers_dict)
        question = MultipleChoiceQuestion(question_text, comment, answers)
        questions.append(question)
    return questions


def _create_answers(answers_dict: dict) -> List[MultipleChoiceAnswer]:
    num_of_answers = answers_dict['num_of_answers']
    answers = []
    for j in range(1, num_of_answers + 1):
        key = 'answer' + str(j)
        answer_dict = answers_dict[key]
        text = answer_dict['answer']
        is_correct = answer_dict['is_correct']
        is_selected = answer_dict['is_selected']
        answer = MultipleChoiceAnswer(text, is_correct, is_selected)
        answers.append(answer)
    return answers
