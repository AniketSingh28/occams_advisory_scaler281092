# tests/test_validation.py

from Backend__.app.utils import is_valid_email, is_valid_phone

def test_email_valid():
    assert is_valid_email("test@example.com")

def test_email_invalid():
    assert not is_valid_email("wrongemail")

def test_phone_valid():
    assert is_valid_phone("+91 9874561230")

def test_phone_invalid():
    assert not is_valid_phone("abc123")
