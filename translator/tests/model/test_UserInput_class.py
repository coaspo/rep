import ltrans
import pytest


def test_create_object():
    user_input = ltrans.model.UserInput(r'Good\n morning', 'English',
                                        'Spanish', 1, 0)
    assert user_input.text_lines == r'Good\n morning'
    assert user_input.src_language == 'English'
    assert user_input.dest_language == 'Spanish'
    assert user_input.is_add_src == 1
    assert user_input.is_add_transliteration == 0
    assert user_input.description == 'translated simple phrase'

def test_create_object():
    # illustrate typical properties
    user_input = ltrans.model.UserInput(r'Good\n morning', 'English',
                                        'Spanish', 1, 0)
    user_input._text_lines = 'Hello'
    assert user_input._text_lines == 'Hello'
    assert user_input.text_lines == 'Hello'

    with pytest.raises(AttributeError):
        user_input.text_lines = 'Hi'
