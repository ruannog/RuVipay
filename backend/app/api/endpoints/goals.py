from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse, GoalSummary
from app.services.goal_service import (
    get_goals_by_user, get_goal_by_id, create_goal, update_goal, 
    delete_goal, get_goals_summary
)

# User ID padrão (sem autenticação)
DEFAULT_USER_ID = 1

router = APIRouter()

@router.get("/", response_model=List[GoalResponse])
def get_user_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter todas as metas do usuário"""
    goals = get_goals_by_user(db, DEFAULT_USER_ID)
    return goals[skip:skip+limit]

@router.get("/summary", response_model=GoalSummary)
def get_goal_summary(
    db: Session = Depends(get_db)
):
    """Obter resumo das metas"""
    return get_goals_summary(db, DEFAULT_USER_ID)

@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):
    """Obter uma meta específica"""
    goal = get_goal_by_id(db, goal_id, DEFAULT_USER_ID)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal

@router.post("/", response_model=GoalResponse)
def create_new_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db)
):
    """Criar uma nova meta"""
    return create_goal(db, goal, DEFAULT_USER_ID)

@router.put("/{goal_id}", response_model=GoalResponse)
def update_existing_goal(
    goal_id: int,
    goal_update: GoalUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar uma meta"""
    goal = update_goal(db, goal_id, goal_update, DEFAULT_USER_ID)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal

@router.delete("/{goal_id}")
def delete_existing_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):
    """Deletar uma meta"""
    success = delete_goal(db, goal_id, DEFAULT_USER_ID)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return {"message": "Goal deleted successfully"}