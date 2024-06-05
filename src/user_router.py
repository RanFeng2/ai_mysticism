from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .models import User
from .models import UserCreate, UserRead
from .database import get_db
from .limiter import get_password_hash, verify_password

# 初始化API路由器
router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # print("user", user,"db", db)
    db_user = db.query(User).filter(User.Username == user.user_name).first()
    # print("db_user1=", db_user)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.PasswordHash)
    db_user = User(Username=user.user_name, Email=user.Email, PasswordHash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # print("db_user2=", db_user)
    return {"message": "Register successful", "db_user": db_user}


# 定义读取单个用户信息的路由，根据账号密码，使用POST方法
@router.post("/login/")
def user_login(user: UserCreate, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = db.query(User).filter(User.Username == user.user_name).first()

    if not verify_password(user.PasswordHash, db_user.PasswordHash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # print(db_user)
    return {"message": "Login successful", "db_user": db_user}



# # 定义读取单个用户信息的路由，根据id，使用GET方法
# @router.get("/users/{user_id}")
# # 用户读取函数，接收用户ID和数据库会话作为参数
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     """
#     根据用户ID从数据库中获取用户信息。
    
#     参数:
#     - user_id: 用户的唯一标识符。
#     - db: 数据库会话，用于执行数据库查询。
    
#     返回:
#     - UserDisplay模型实例，包含用户显示信息。
    
#     如果用户不存在，则抛出HTTPException异常，状态码为404，详情为"User not found"。
#     """
#     # 根据用户ID查询数据库中的用户信息
#     db_user = db.query(User).filter(User.id == user_id).first()
#     # 如果用户不存在，则抛出HTTP异常，提示用户未找到
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     # 返回查询到的用户信息
#     return db_user