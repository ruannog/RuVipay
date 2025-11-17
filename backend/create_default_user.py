"""
Script para criar usuário padrão no sistema
"""
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.services.auth import get_password_hash

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar sessão
db = SessionLocal()

try:
    # Verificar se usuário já existe
    existing_user = db.query(User).filter(User.id == 1).first()
    
    if not existing_user:
        # Criar usuário padrão
        default_user = User(
            id=1,
            username="admin",
            email="admin@ruviopay.com",
            full_name="Administrador",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        
        print("✅ Usuário padrão criado com sucesso!")
        print(f"   ID: {default_user.id}")
        print(f"   Username: {default_user.username}")
        print(f"   Email: {default_user.email}")
    else:
        print("ℹ️ Usuário padrão já existe!")
        print(f"   ID: {existing_user.id}")
        print(f"   Username: {existing_user.username}")
        print(f"   Email: {existing_user.email}")
        
except Exception as e:
    print(f"❌ Erro ao criar usuário: {e}")
    db.rollback()
finally:
    db.close()
