from quz.persistence import AbstractPersistence
from quz.quiz import Quiz

import logging

log = logging.getLogger(__name__)


class Model:
    def __init__(self, config: dict, persistence: AbstractPersistence):
        self._config = config
        self._persistence = persistence

    @property
    def persistence(self) -> AbstractPersistence:
        return self._persistence

    def save_quiz(self, marked_user_input: str) -> str:
        quiz = Quiz(marked_user_input=marked_user_input)
        status_msg = self.persistence.save(quiz)
        return status_msg

    def next_quiz(self) -> tuple:
        status_msg, persistence_msg, quiz = self.persistence.get_next()
        return status_msg, persistence_msg, quiz

    def previous_quiz(self) -> tuple:
        status_msg, persistence_msg, quiz = self.persistence.get_previous()
        return status_msg, persistence_msg, quiz

    def delete_quiz(self) -> tuple:
        status_msg, persistence_msg = self.persistence.delete()
        return status_msg, persistence_msg

    def update_quiz(self,  marked_user_input: str) -> tuple:
        quiz = Quiz(marked_user_input=marked_user_input)
        status_msg, persistence_msg = self.persistence.update(quiz)
        return status_msg, persistence_msg


