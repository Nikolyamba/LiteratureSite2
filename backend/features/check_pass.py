import re

async def check_password(password: str) -> bool:
    pattern = r"^(?=.*[A-Za-z])(?=.*\d).+$"
    return bool(re.match(pattern, password))