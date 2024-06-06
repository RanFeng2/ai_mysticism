from typing import Optional
from pydantic import BaseModel, Field

from sqlalchemy import Sequence, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

############################################################
# user
############################################################
Base = declarative_base()
class User(Base):
    __tablename__ = 'User'
    UserId = Column(Integer, Sequence('user_id_seq'), primary_key=True, nullable=False)
    Username = Column(String(50), unique=True, index=True)
    Email = Column(String(100), unique=True, index=True)
    PasswordHash = Column(String(100))
    CreateDate = Column(DateTime)

class UserCreate(BaseModel):
    user_name: str
    Email: str
    PasswordHash: str

class UserRead(BaseModel):
    UserId: int
    user_name: str
    Email: str

    class Config:
        orm_mode = True
        from_attributes = True 

############################################################
# query
############################################################
class Divination(Base):
    __tablename__ = 'DivinationResult'
    ResultId = Column(Integer, Sequence('result_id_seq'), primary_key=True)
    UserId = Column(Integer)
    Question = Column(String(500))
    Result = Column(String(500))
    DivinationType = Column(String(500))
    DivinationDate	= Column(DateTime)

class DivinationCreate(BaseModel):
    UserId: int
    Question: str
    Result: str
    DivinationType: str

class DivinationRead(BaseModel):
    UserId: int
    


############################################################

class SettingsInfo(BaseModel):
    login_type: str
    user_name: str
    rate_limit: str
    user_rate_limit: str
    ad_client: str = ""
    ad_slot: str = ""
    enable_login: bool = False
    enable_rate_limit: bool = False
    database_url: str


class OauthBody(BaseModel):
    login_type: str
    code: Optional[str]

class NewName(BaseModel):
    surname: str
    sex: str
    birthday: str
    new_name_prompt: str


class PlumFlower(BaseModel):
    num1: int
    num2: int


class Fate(BaseModel):
    name1: str
    name2: str


class DivinationBody(BaseModel):
    prompt: str
    prompt_type: str
    birthday: str
    new_name: Optional[NewName] = None
    plum_flower: Optional[PlumFlower] = None
    fate: Optional[Fate] = None


class BirthdayBody(BaseModel):
    birthday: str = Field(example="2000-08-17 00:00:00")


class CommonResponse(BaseModel):
    content: str
    request_id: str

