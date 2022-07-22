
def password_check(password: str) -> list:
    warnings = list()
    if len(password) < 8:
        warnings.append("Password less than 8 chars")
    if not password.isalnum():
        warnings.append("Password must contain not less 1 digit and 1 char")
    return warnings
