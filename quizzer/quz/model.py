import logging
from typing import List

from quz.persistence import FilePersistence
from quz.quiz import Quiz

log = logging.getLogger(__name__)


def _create_domain_object(data_dict: dict) -> Quiz:
    return Quiz(quiz_data_dict=data_dict)


class Model:
    def __init__(self, quiz_dir: str):
        self._persistence = FilePersistence(quiz_dir)
        self._quiz: Quiz = self._persistence.get(_create_domain_object)

    @property
    def latest_quiz_topic(self) -> str:
        return self._persistence.latest_topic

    @property
    def quiz(self) -> Quiz:
        return self._quiz

    @property
    def quiz_description(self) -> str:
        return self._persistence.description

    @property
    def quiz_topics(self) -> List[str]:
        return self._persistence.topics

    @property
    def status_msg(self) -> str:
        return self._persistence.status

    def create_new_quiz(self, marked_user_input: str):
        self._quiz = Quiz(marked_user_input=marked_user_input)

    def delete_quiz(self) -> (str, str):
        status_msg = self._persistence.delete()
        status_msg2, persistence_msg, self._quiz = self._persistence.get(_create_domain_object)
        return status_msg + status_msg2, persistence_msg

    def set_to_next_quiz(self) -> (str, str, Quiz):
        self._quiz = self._persistence.get_next(_create_domain_object)

    def set_to_previous_quiz(self) -> (str, str, Quiz):
        self._quiz = self._persistence.get_previous(_create_domain_object)

    def get_quiz(self) -> Quiz or dict:
        self._quiz = self._persistence.get(_create_domain_object)
        return self._quiz

    def reset_quiz_topic(self, quiz_topic: str) -> (str, str, Quiz):
        self._persistence.reset(quiz_topic)
        status_msg, persistence_msg, self._quiz = self._persistence.get_previous(_create_domain_object)
        return status_msg, persistence_msg, self._quiz

    def save_quiz(self, quiz_topic: str):
        self._persistence.save(quiz_topic, self._quiz.get_data_dict())

    def set_answer(self, answer_index, is_selected):
        self._persistence.save(quiz_topic, self._quiz.get_data_dict())

    def update_quiz(self, marked_user_input: str) -> (str, str):
        self._quiz = Quiz(marked_user_input=marked_user_input)
        status_msg, persistence_msg = self._persistence.update(self._quiz.get_data_dict())
        return status_msg, persistence_msg
