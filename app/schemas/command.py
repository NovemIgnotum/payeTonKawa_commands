from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommandBase(BaseModel):
    id_customers: int
    id_product: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CommandCreate(CommandBase):
    pass

class CommandUpdate(BaseModel):
    id_customers: int
    id_product: int

class CommandInDB(CommandBase):
    id: int

    

    class Config:
        from_attributes = True

class Command(CommandInDB):
    pass


class CommandResponse(BaseModel):
    message: str
    command: CommandInDB

    class Config:
        from_attributes = True
        
class getResponse(BaseModel):
    message: str
    command: list[CommandInDB]

    class Config:
        from_attributes = True