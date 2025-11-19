# backend/app/utils.py
import re
email_re = re.compile(r"[\w\.-]+@[\w\.-]+")
phone_re = re.compile(r"\+?[0-9][0-9\- ()]{5,20}")


def is_valid_email(s: str) -> bool:
    return bool(email_re.match(s))


def is_valid_phone(s: str) -> bool:
    return bool(phone_re.match(s))