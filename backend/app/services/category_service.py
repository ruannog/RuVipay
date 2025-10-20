from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def get_categories_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).filter(
        Category.user_id == user_id,
        Category.is_active == True
    ).offset(skip).limit(limit).all()

def get_categories_by_type(db: Session, user_id: int, category_type: str) -> List[Category]:
    return db.query(Category).filter(
        Category.user_id == user_id,
        Category.type == category_type,
        Category.is_active == True
    ).all()

def get_category_by_id(db: Session, category_id: int, user_id: int) -> Optional[Category]:
    return db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

def create_category(db: Session, category: CategoryCreate, user_id: int) -> Category:
    db_category = Category(**category.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: CategoryUpdate, user_id: int) -> Optional[Category]:
    db_category = get_category_by_id(db, category_id, user_id)
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    db_category = get_category_by_id(db, category_id, user_id)
    if not db_category:
        return False
    
    # Soft delete
    db_category.is_active = False
    db.commit()
    return True

def create_default_categories(db: Session, user_id: int):
    """Cria categorias padrão para um novo usuário"""
    default_categories = [
        # Categorias de Receita
        {"name": "Salário", "type": "income", "icon": "💼", "color": "#10B981"},
        {"name": "Freelance", "type": "income", "icon": "💻", "color": "#059669"},
        {"name": "Investimentos", "type": "income", "icon": "📈", "color": "#047857"},
        {"name": "Outros", "type": "income", "icon": "💰", "color": "#065F46"},
        
        # Categorias de Despesa
        {"name": "Alimentação", "type": "expense", "icon": "🍕", "color": "#EF4444"},
        {"name": "Transporte", "type": "expense", "icon": "🚗", "color": "#DC2626"},
        {"name": "Moradia", "type": "expense", "icon": "🏠", "color": "#B91C1C"},
        {"name": "Saúde", "type": "expense", "icon": "🏥", "color": "#991B1B"},
        {"name": "Educação", "type": "expense", "icon": "📚", "color": "#7F1D1D"},
        {"name": "Lazer", "type": "expense", "icon": "🎮", "color": "#6B1D1D"},
        {"name": "Compras", "type": "expense", "icon": "🛒", "color": "#5B1D1D"},
    ]
    
    for cat_data in default_categories:
        category = CategoryCreate(**cat_data)
        create_category(db, category, user_id)