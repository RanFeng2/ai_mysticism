from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import User
from .database import get_db

# 初始化密码处理器，使用bcrypt算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 配置用于获取JWT的OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 函数：加密密码
def hash_password(password: str) -> str:
    """使用bcrypt算法加密密码"""
    return pwd_context.hash(password)

# 函数：验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)

# 函数：认证用户
def authenticate_user(db: Session, username: str, password: str) -> User:
    """验证用户的用户名和密码，返回用户对象或None"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# 函数：创建JWT
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """生成一个JWT，有效期默认为15分钟"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
    return encoded_jwt

# 函数：获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """解析JWT，从数据库获取并返回当前用户对象"""
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


import datetime
import logging
from typing import Optional
import jwt

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import settings
from src.models import User
from fastapi import HTTPException

_logger = logging.getLogger(__name__)
security = HTTPBearer()
DEFAULT_TOKEN = ["xxx", "undefined"]
def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[User]:
    try:
        jwt_token = credentials.credentials
        if not jwt_token or jwt_token in DEFAULT_TOKEN:
            return
        payload = jwt.decode(
            jwt_token, settings.jwt_secret, algorithms=["HS256"])
        jwt_payload = User.parse_obj(payload)
        if jwt_payload.expire_at < datetime.datetime.now().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        return jwt_payload
    except Exception:
        return
    