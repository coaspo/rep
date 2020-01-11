class QuizDataError(Exception):
    pass


def create_questions(text: str) -> list:
    questions = []
    text_lines = text.strip().split('\n')
    if len(text_lines) < 4:
        raise QuizDataError('Invalid text; line count < 4')
    question_text = None
    answers = None
    comment = None

    for i, line in enumerate(text_lines):
        line = line.strip()
        if len(line) == 0:
            continue

        if line.startswith('?'):
            if question_text is not None:
                question = Question(question_text, answers, comment)
                questions.append(question)
            question_text = line[1:]
            answers = []
            comment = None
        elif line.startswith('+'):
            answers.append(Answer(line[1:], True))
        elif line.startswith('-'):
            answers.append(Answer(line[1:], False))
        elif line.startswith('='):
            if comment is not None:
                raise QuizDataError(f'More than one comment for question;  line#{i}; line={line}')
            comment = line[1:]
        else:
            raise QuizDataError(f'First character is not: ?+-=  line#{i}; line={line}')

    question = Question(question_text, answers, comment)
    questions.append(question)
    return questions


class Quiz(dict):
    def __init__(self, marked_user_input: str, latest_question_index: int = 0, questions: list = None):
        self._marked_user_input = marked_user_input
        self._questions = create_questions(marked_user_input) if questions is None else questions
        self._latest_question_index = latest_question_index

    @property
    def marked_user_input(self) -> str:
        return self._marked_user_input

    @property
    def questions(self) -> list:
        return self._questions

    def question(self) -> int:
        return self._questions[self._latest_question_index]

    def next_question(self) -> int:
        if self._latest_question_index + 1 < len(self._questions):
            self._latest_question_index += 1
        return self._questions[self._latest_question_index]

    def previous_question(self) -> int:
        if self._latest_question_index != 0:
            self._latest_question_index -= 1
        return self._questions[self._latest_question_index]

    def score(self) -> tuple:
        correct_questions = [q for q in self._questions if q.are_all_answers_correct]
        ratio = f'{len(correct_questions)}/{len(self._questions)}'
        percent = round(100. * len(correct_questions) / len(self._questions))
        return ratio, f'{percent}%'

    def __str__(self) -> str:
        return f'Quiz: questions = {self._questions}'


class Question:
    def __init__(self, statement: str, answers: list, comment: str = None):
        if len(answers) < 2:
            raise QuizDataError(f'Less than 2 possible answers;  answers={answers}\n statement={statement}')
        self._statement = statement
        self._answers = answers
        self._comment = comment

    @property
    def statement(self) -> str:
        return self._statement

    @property
    def answers(self) -> list:
        return self._answers

    @property
    def comment(self) -> str:
        return self._comment


    def are_all_answers_correct(self) -> bool:
        for answer in self._answers:
            if (answer.is_correct and not answer.is_selected) or \
                    (not answer.is_correct and answer.is_selected):
                return False
        return True

    def __str__(self) -> str:
        return f'Question: statement={self._statement}  answers={self._answers}  comment={self._comment}'

    def __repr__(self) -> str:
        return self.__str__()


class Answer:
    def __init__(self, solution: str, is_correct: bool, is_selected: bool = False):
        self._solution = solution
        self._is_correct = is_correct
        self._is_selected = is_selected

    @property
    def solution(self) -> str:
        return self._solution

    @property
    def is_correct(self) -> str:
        return self._is_correct

    @property
    def is_selected(self) -> str:
        return self._is_selected

    def __str__(self) -> str:
        return f'Answer: is_correct={self.is_correct}  is_selected={self._is_selected} solution={self._solution}'

    def __repr__(self) -> str:
        return self.__str__()
