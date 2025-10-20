from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import (
    get_categories_by_user, get_categories_by_type, get_category_by_id,
    create_category, update_category, delete_category
)
from app.api.endpoints.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_user_categories(
    category_type: str = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter todas as categorias do usuário"""
    if category_type:
        return get_categories_by_type(db, current_user.id, category_type)
    return get_categories_by_user(db, current_user.id)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter uma categoria específica"""
    category = get_category_by_id(db, category_id, current_user.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.post("/", response_model=CategoryResponse)
def create_new_category(
    category: CategoryCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar uma nova categoria"""
    return create_category(db, category, current_user.id)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar uma categoria"""
    category = update_category(db, category_id, category_update, current_user.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.delete("/{category_id}")
def delete_existing_category(
    category_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar uma categoria"""
    success = delete_category(db, category_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return {"message": "Category deleted successfully"}