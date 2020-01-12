import pytest
import pprint
import quz


def test_create_questions():
    marked_user_input = '?What is 2+3\n' \
                        '-is 4\n' \
                        '+is 5\n\n' \
                        '=addition\n\n' \
 \
                        '?1*2 = ?\n' \
                        '- = 1\n' \
                        '+ = 2\n' \
                        '- = 4\n' \
 \
                        '?What is 12+13\n' \
                        '-is 24\n' \
                        '+is 25\n\n' \
                        '=big addition\n\n'

    data_dict = quz.quiz._create_data_dict(marked_user_input)
    expected_data_dict = {'latest_question_num': 1,
                          'num_of_completed_questions': 0,
                          'num_of_questions': 3,
                          'marked_user_input': marked_user_input,
                          'question1': 'What is 2+3',
                          'question1_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': 'is 4'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': 'is 5'},
                                                'comment': 'addition',
                                                'num_of_answers': 2},
                          'question2': '1*2 = ?',
                          'question2_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': ' = 1'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': ' = 2'},
                                                'answer3': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': ' = 4'},
                                                'num_of_answers': 3},
                          'question3': 'What is 12+13',
                          'question3_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': 'is 24'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': 'is 25'},
                                                'comment': 'big addition',
                                                'num_of_answers': 2}}

    pp_data_dict = pprint.pformat(data_dict).split('\n')
    pp_expected_data_dict = pprint.pformat(expected_data_dict).split('\n')

    for i, line in enumerate(pp_data_dict):
        print(i, line)
        if i > len(pp_expected_data_dict) - 1:
            raise Exception(f'Actual larger than expected.\nactual/expected:\n{pp_data_dict}{pp_expected_data_dict}')
        if line != pp_expected_data_dict[i]:
            pytest.fail(f'json lines #{i} not equal ' +
                        f'\nactual/expected lines:\n{line}\n{pp_expected_data_dict[i]}' +
                        f'\nactual/expected DICTs:\n{data_dict}\n{expected_data_dict}')
