
from email_core.organizer import detect_provider


def test_detect_gmail():
    assert detect_provider("user@gmail.com") == "gmail"


def test_detect_outlook():
    assert detect_provider("user@hotmail.com") == "outlook"


def test_detect_unknown_domain():
    assert detect_provider("user@example.com") == "unknown"


def test_detect_invalid_format():
    assert detect_provider("user.gmail.com") == "unknown"


def test_detect_case_insensitive():
    assert detect_provider("USER@GMAIL.COM") == "gmail"


def test_detect_whitespace():
    assert detect_provider(" user@gmail.com ") == "gmail"

