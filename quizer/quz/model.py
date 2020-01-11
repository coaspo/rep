from quz.persistence import AbstractPersistence

import logging


log = logging.getLogger(__name__)


class Model:
    def __init__(self, config: dict, persistence: AbstractPersistence):
        self._config = config
        self._persistence = persistence

    @property
    def persistence(self) -> AbstractPersistence:
        return self._persistence

    def create_quiz(self, text: str) -> str:
         if log.isEnabledFor(logging.DEBUG):
            log.debug(text)
         return None

    def save_quiz(self, text: str) -> str:
        status_msg = self.persistence.save_quiz(text)
        return status_msg

    def next_quiz(self) -> tuple:
        status_msg, persistence_msg, translation = self.persistence.get_next()
        return status_msg, persistence_msg, translation

    def previous_quiz(self) -> tuple:
        status_msg, persistence_msg, translation = self.persistence.get_previous()
        return status_msg, persistence_msg, translation

    def delete_quiz(self) -> tuple:
        status_msg, persistence_msg = self.persistence.delete()
        return status_msg, persistence_msg

    def update_quiz(self, text: str) -> tuple:
        status_msg, persistence_msg = self.persistence.update(text)
        return status_msg, persistence_msg


def create_quiz(text: str) -> str:
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'text={text}')


