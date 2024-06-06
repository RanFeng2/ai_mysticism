from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .models import Divination
from .models import DivinationCreate, DivinationRead
from .database import get_db
from .limiter import get_password_hash, verify_password
from datetime import datetime

# 初始化API路由器
router = APIRouter()

# 保存一个用户query，根据userid,使用POST方法
@router.post("/save/")
def create_Divination(divination: DivinationCreate, db: Session = Depends(get_db)):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 转换为字符串
    
    db_divination = Divination(UserId=divination.UserId, 
                               Question=divination.Question,
                               Result=divination.Result,
                               DivinationType=divination.DivinationType,
                               DivinationDate=current_time)
    db.add(db_divination)
    db.commit()
    db.refresh(db_divination)
    return {"message": "Query Save successful", "db_divination": db_divination}


# 定义读取单个用户的所有query，根据userid，使用POST方法
@router.post("/queryall/")
def list_Divination(divination: DivinationRead, db: Session = Depends(get_db)):
    if divination is None:
        raise HTTPException(status_code=404, detail="Divination not found")
    
    print("Divination.UserId=", Divination.UserId)
    print("divination.UserId=", divination.UserId)

    db_divination = db.query(Divination).filter(Divination.UserId == divination.UserId).all()

    print("db_Divination=", db_divination)

    return {"message": "Query successful", "db_Divination": db_divination}
    


