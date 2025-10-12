from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Category
from app.schemas.schemas import Category as CategorySchema, CategoryCreate, CategoryUpdate
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CategorySchema])
async def get_categories(
    type: str = None,  # 'receita' ou 'despesa'
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Buscar todas as categorias do usuário"""
    query = db.query(Category).filter(Category.user_id == current_user.id)
    
    if type:
        query = query.filter(Category.type == type)
    
    categories = query.all()
    return categories

@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Buscar uma categoria específica"""
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    return category

@router.post("/", response_model=CategorySchema)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Criar uma nova categoria"""
    # Verificar se já existe uma categoria com o mesmo nome e tipo
    existing_category = db.query(Category).filter(
        Category.name == category.name,
        Category.type == category.type,
        Category.user_id == current_user.id
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma categoria com esse nome e tipo"
        )
    
    db_category = Category(
        **category.dict(),
        user_id=current_user.id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Atualizar uma categoria"""
    db_category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Atualizar apenas os campos fornecidos
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deletar uma categoria"""
    db_category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Verificar se há transações usando esta categoria
    from app.models.models import Transaction
    transactions_count = db.query(Transaction).filter(
        Transaction.category_id == category_id
    ).count()
    
    if transactions_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Não é possível deletar categoria que possui transações"
        )
    
    db.delete(db_category)
    db.commit()
    
    return {"message": "Categoria deletada com sucesso"}