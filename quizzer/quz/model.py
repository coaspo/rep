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
        _, _, self._quiz = self._persistence.get(_create_domain_object)

    def current_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, self._quiz = self._persistence.get(_create_domain_object)
        return status_msg, persistence_msg, self._quiz

    def delete_quiz(self) -> (str, str):
        status_msg = self._persistence.delete()
        status_msg2, persistence_msg, self._quiz = self._persistence.get(_create_domain_object)
        return status_msg + status_msg2, persistence_msg

    def quiz_description(self) -> str:
        return self._persistence.description()

    @property
    def latest_quiz_topic(self) -> str:
        return self._persistence.latest_topic()

    def next_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, self._quiz = self._persistence.get_next(_create_domain_object)
        return status_msg, persistence_msg, self._quiz

    def previous_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, self._quiz = self._persistence.get_previous(_create_domain_object)
        return status_msg, persistence_msg, self._quiz

    @property
    def quiz(self) -> Quiz:
        return self._quiz

    def quiz_description_old(self) -> str:
        if self._quiz is None:
            return ''
        return self._persistence.description_old()

    def quiz_description(self) -> str:
        if self._quiz is None:
            return ''
        return self._persistence.description()

    @property
    def quiz_topics(self) -> List[str]:
        return self._persistence.topics()

    def create_new_quiz(self, marked_user_input: str):
        self._quiz = Quiz(marked_user_input=marked_user_input)

    def reset_quiz_topic(self, quiz_topic: str) -> (str, str, Quiz):
        self._persistence.reset(quiz_topic)
        status_msg, persistence_msg, self._quiz = self._persistence.get_previous(_create_domain_object)
        return status_msg, persistence_msg, self._quiz

    def save_quiz(self, quiz_topic: str):
        self._persistence.save(quiz_topic, self._quiz.get_data_dict())

    @property
    def status_msg(self) -> str:
        return self._persistence.status

    def update_quiz(self, marked_user_input: str) -> (str, str):
        self._quiz = Quiz(marked_user_input=marked_user_input)
        status_msg, persistence_msg = self._persistence.update(self._quiz.get_data_dict())
        return status_msg, persistence_msg
