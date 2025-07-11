from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_pass(password:str,hashed_password:str):
    return pwd_context.verify(password, hashed_password)