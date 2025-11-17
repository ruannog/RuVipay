from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class InvestmentBase(BaseModel):
    name: str
    type: str  # 'stocks', 'crypto', 'funds', 'real_estate', etc
    amount_invested: float
    current_value: float
    purchase_date: datetime
    description: Optional[str] = None

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    amount_invested: Optional[float] = None
    current_value: Optional[float] = None
    purchase_date: Optional[datetime] = None
    description: Optional[str] = None

class InvestmentResponse(InvestmentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    profit_loss: Optional[float] = None
    profit_loss_percentage: Optional[float] = None
    
    @validator('profit_loss', always=True)
    def calculate_profit_loss(cls, v, values):
        """Calcula lucro/prejuízo do investimento"""
        current_value = values.get('current_value', 0)
        amount_invested = values.get('amount_invested', 0)
        return current_value - amount_invested
    
    @validator('profit_loss_percentage', always=True)
    def calculate_profit_loss_percentage(cls, v, values):
        """Calcula percentual de lucro/prejuízo"""
        current_value = values.get('current_value', 0)
        amount_invested = values.get('amount_invested', 0)
        if amount_invested > 0:
            return ((current_value - amount_invested) / amount_invested) * 100
        return 0.0
    
    class Config:
        from_attributes = True