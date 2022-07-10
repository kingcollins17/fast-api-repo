from fastapi import HTTPException,Depends,status
from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = '02332gfhddfdju383he39f39fhha62eovng90454234k2240'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_token(data: dict) -> str:
     copy = data.copy()
     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     copy.update({"exp":expire})

     jwt_token = jwt.encode(copy,SECRET_KEY,algorithm=ALGORITHM)
     return jwt_token

def verify_token(token: str, cred_exception: HTTPException):
     try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
          user_email = payload.get("user_email")
          if not user_email:
               raise cred_exception
     except JWTError:
          raise cred_exception
     return user_email

def get_current_user(token:str = Depends(oauth2_scheme)):
     cred_exp = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail=f"could not validate credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
     return verify_token(token,cred_exp)
     

