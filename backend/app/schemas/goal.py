from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class GoalBase(BaseModel):
    title: str
    goal_type: str  # 'economia', 'investimento', 'compra', 'viagem', 'outros'
    target_amount: float
    current_amount: float = 0.0
    period_type: str  # 'mensal', 'anual', 'livre'
    start_date: datetime
    end_date: datetime
    category_id: Optional[int] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    goal_type: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    period_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category_id: Optional[int] = None

class GoalResponse(GoalBase):
    id: int
    user_id: int
    progress_percentage: Optional[float] = None
    remaining_amount: Optional[float] = None
    is_completed: Optional[bool] = None
    
    @validator('progress_percentage', always=True)
    def calculate_progress_percentage(cls, v, values):
        """Calcula percentual de progresso da meta"""
        target = values.get('target_amount', 0)
        current = values.get('current_amount', 0)
        if target > 0:
            return min((current / target) * 100, 100.0)
        return 0.0
    
    @validator('remaining_amount', always=True)
    def calculate_remaining_amount(cls, v, values):
        """Calcula valor restante para atingir a meta"""
        target = values.get('target_amount', 0)
        current = values.get('current_amount', 0)
        return max(target - current, 0.0)
    
    @validator('is_completed', always=True)
    def calculate_is_completed(cls, v, values):
        """Verifica se a meta foi concluída"""
        target = values.get('target_amount', 0)
        current = values.get('current_amount', 0)
        return current >= target
    
    class Config:
        orm_mode = True

class GoalSummary(BaseModel):
    """Resumo das metas do usuário"""
    total_goals: int
    active_goals: int
    completed_goals: int
    total_target_amount: float
    total_current_amount: float
    overall_progress_percentage: float