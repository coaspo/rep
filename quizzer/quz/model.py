import json
import os
import re

from quz.persistence import AbstractPersistence
from quz.quiz import Quiz

import logging

log = logging.getLogger(__name__)


def _create_domain_object(data_dict: dict) -> dict:
    return Quiz(quiz_data_dict=data_dict)


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
        status_msg, persistence_msg, quiz = self.persistence.get_next(_create_domain_object)
        return status_msg, persistence_msg, quiz

    def previous_quiz(self) -> (str, str, Quiz):
        status_msg, persistence_msg, quiz = self.persistence.get_previous(_create_domain_object)
        return status_msg, persistence_msg, quiz

    def delete_quiz(self) -> (str, str):
        status_msg, persistence_msg = self.persistence.delete()
        return status_msg, persistence_msg

    def update_quiz(self, marked_user_input: str) -> (str, str):
        quiz = Quiz(marked_user_input=marked_user_input)
        status_msg, persistence_msg = self.persistence.update(quiz)
        return status_msg, persistence_msg


def quiz_categories(quizzes_dir) -> list:
    absolute_quizzes_dir = _find_absolute_dir_path(quizzes_dir)

    latest_category = _find_latest_quiz_category(absolute_quizzes_dir)
    categories = _find_quiz_categories(absolute_quizzes_dir)

    if len(categories) == 0:
        categories = ['quiz']
    if latest_category is None:
        latest_category = categories[0]

    return latest_category, categories


def _find_quiz_categories(absolute_quizzes_dir):
    categories = []
    for file in sorted(os.listdir(absolute_quizzes_dir)):
        if file == 'latest_work.json':
            continue
        if file.endswith('.json'):
            category = re.split(r'\.|-', file)[0]
            if category not in categories:
                categories.append(category)
    return categories


def _find_latest_quiz_category(absolute_quizzes_dir):
    file_path = absolute_quizzes_dir + "/latest_work.json"
    latest_category = None
    if os.path.exists(file_path):
        with open(file_path) as f:
            latest_work = json.load(f)
        latest_category = latest_work['LATEST_QUIZ_CATEGORY']
    return latest_category


def _find_absolute_dir_path(dir_path):
    absolute_dir = dir_path
    if dir_path.startswith("./"):
        absolute_dir = os.path.dirname(__file__) + absolute_dir[1:]
    absolute_dir = os.path.abspath(absolute_dir)
    return absolute_dir
