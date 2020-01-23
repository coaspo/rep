from quz.persistence import FilePersistence
from quz.quiz import Quiz
import logging

log = logging.getLogger(__name__)


def _create_domain_object(data_dict: dict) -> Quiz:
    return Quiz(quiz_data_dict=data_dict)


class Model:
    def __init__(self, quiz_dir: str):
        self._persistence = FilePersistence(quiz_dir)

    def save_quiz(self, quiz_topic: str, marked_user_input: str) -> str:
        quiz = Quiz(quiz_topic=quiz_topic, marked_user_input=marked_user_input)
        status_msg = self._persistence.save(quiz_topic, quiz.data_dict())
        return status_msg

    def next_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, quiz = self._persistence.get_next(_create_domain_object)
        return status_msg, persistence_msg, quiz

    def previous_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, quiz = self._persistence.get_previous(_create_domain_object)
        return status_msg, persistence_msg, quiz

    def delete_quiz(self) -> (str, str):
        status_msg, persistence_msg = self._persistence.delete()
        return status_msg, persistence_msg

    def update_quiz(self, marked_user_input: str) -> (str, str):
        quiz = Quiz(marked_user_input=marked_user_input)
        status_msg, persistence_msg = self._persistence.update(quiz.data_dict())
        return status_msg, persistence_msg

    def reset_persistence(self, quiz_topic: str) -> None:
        self._persistence.reset(quiz_topic)

    @property
    def latest_quiz_topic(self) -> str:
        return self._persistence.latest_topic()

    @property
    def quiz_topics(self) -> list:
        return self._persistence.topics()
