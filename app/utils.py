from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_it(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(input_password: str, user_password: str) -> bool:
    return pwd_context.verify(input_password, user_password)
