from quz.persistence import AbstractPersistence
from quz.quiz import Quiz

import logging

log = logging.getLogger(__name__)


def create_domain_object(data_dict: dict) -> dict:
    return Quiz(quiz_data=data_dict)


class Model:
    def __init__(self, persistence: AbstractPersistence):
        self._persistence = persistence

    @property
    def persistence(self) -> AbstractPersistence:
        return self._persistence

    def save_quiz(self, marked_user_input: str) -> str:
        quiz = Quiz(marked_user_input=marked_user_input)
        status_msg = self.persistence.save(quiz)
        return status_msg

    def next_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, quiz = self.persistence.get_next(create_domain_object)
        return status_msg, persistence_msg, quiz

    def previous_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, quiz = self.persistence.get_previous(create_domain_object)
        return status_msg, persistence_msg, quiz

    def delete_quiz(self) -> (str, str):
        status_msg, persistence_msg = self.persistence.delete()
        return status_msg, persistence_msg

    def update_quiz(self, marked_user_input: str) -> (str, str):
        quiz = Quiz(marked_user_input=marked_user_input)
        status_msg, persistence_msg = self.persistence.update(quiz)
        return status_msg, persistence_msg


