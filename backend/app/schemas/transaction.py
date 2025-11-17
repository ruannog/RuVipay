from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class TransactionBase(BaseModel):
    description: str
    amount: Decimal
    type: str  # 'income' ou 'expense'
    date: datetime
    notes: Optional[str] = None
    category_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    type: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None
    category_id: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[str] = None  # Nome da categoria
    
    class Config:
        from_attributes = True