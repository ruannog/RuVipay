from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Schemas para User
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para Category
class CategoryBase(BaseModel):
    name: str
    type: str  # 'receita' ou 'despesa'
    color: Optional[str] = "#3498db"
    icon: Optional[str] = "💰"

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None

class Category(CategoryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas para Transaction
class TransactionBase(BaseModel):
    description: str
    amount: float
    type: str  # 'receita' ou 'despesa'
    date: datetime
    is_recurring: Optional[bool] = False
    is_completed: Optional[bool] = True
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    category_id: int

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    is_completed: Optional[bool] = None
    notes: Optional[str] = None
    category_id: Optional[int] = None

class Transaction(TransactionBase):
    id: int
    user_id: int
    category_id: int
    category: Category
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para Budget
class BudgetBase(BaseModel):
    name: str
    amount: float
    period: str  # 'monthly', 'yearly'

class BudgetCreate(BudgetBase):
    category_id: Optional[int] = None

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    period: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class Budget(BudgetBase):
    id: int
    user_id: int
    category_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para Dashboard
class DashboardSummary(BaseModel):
    total_receitas: float
    total_despesas: float
    saldo: float
    transacoes_mes: int

class MonthlyData(BaseModel):
    month: str
    receitas: float
    despesas: float
    saldo: float

class CategorySum(BaseModel):
    category_name: str
    total: float
    color: str

class DashboardData(BaseModel):
    summary: DashboardSummary
    monthly_data: List[MonthlyData]
    receitas_by_category: List[CategorySum]
    despesas_by_category: List[CategorySum]

# Schemas para autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None