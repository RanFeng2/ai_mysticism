import time
import logging

from collections import defaultdict
from fastapi import HTTPException, Request

_logger = logging.getLogger(__name__)
request_limit_map = defaultdict(list)


from passlib.context import CryptContext


def get_real_ipaddr(request: Request) -> str:
    if "x-real-ip" in request.headers:
        return request.headers["x-real-ip"]
    else:
        if not request.client or not request.client.host:
            return "127.0.0.1"

        return request.client.host


def check_rate_limit(key: str, time_window_seconds: int, max_requests: int) -> None:
    cur_timestamp = int(time.time())
    try:
        # remove expired records
        while request_limit_map[key] and request_limit_map[key][0] < (cur_timestamp - time_window_seconds):
            request_limit_map[key].pop(0)
        # add current timestamp
        request_limit_map[key].append(cur_timestamp)
        req_count = len(request_limit_map[key])
        if req_count >= max_requests:
            raise HTTPException(
                status_code=429, detail="Rate limit exceeded"
            )
        return
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        _logger.error(f"Rate limit failed: {e}")
    raise HTTPException(
        status_code=400, detail="Rate limit failed"
    )


# 创建密码上下文，指定使用bcrypt算法，自动弃用旧的算法
# 创建一个密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    对密码进行哈希处理。
    
    使用bcrypt算法对传入的密码字符串进行安全的哈希处理，返回哈希后的字符串。
    这个函数的设计目的是为了安全地存储密码，而不是为了密码的解密。
    
    参数:
    password (str): 需要进行哈希处理的明文密码。
    
    返回:
    str: 经过bcrypt算法哈希处理后的密码字符串。
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确。
    
    通过比较明文密码和哈希后的密码，来验证密码的正确性。这个函数的设计目的是为了安全地验证用户输入的密码，
    而不是为了解密已经哈希的密码。
    
    参数:
    plain_password (str): 用户输入的明文密码。
    hashed_password (str): 哈希后的密码字符串，用于和用户输入的明文密码进行比较。
    
    返回:
    bool: 如果明文密码和哈希后的密码匹配，则返回True，否则返回False。
    """
    return pwd_context.verify(plain_password, hashed_password)
