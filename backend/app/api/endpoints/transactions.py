from typing import List, Optionalfrom typing import List, Optionalfrom fastapi import APIRouter, Depends, HTTPException, status

from fastapi import APIRouter, Depends, HTTPException, status, Query

from datetime import datetimefrom datetime import datetimefrom sqlalchemy.orm import Session

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status, Queryfrom typing import List

from app.database import get_db

from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponsefrom sqlalchemy.orm import Sessionfrom datetime import datetime, timedelta

from app.services.transaction_service import (

    get_transactions_by_user, get_transaction_by_id, create_transaction,from app.database import get_db

    update_transaction, delete_transaction, get_user_balance,

    get_monthly_summary, get_recent_transactionsfrom app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponsefrom app.database import get_db

)

from app.api.endpoints.auth import get_current_userfrom app.services.transaction_service import (from app.models.models import Transaction, Category



router = APIRouter()    get_transactions_by_user, get_transaction_by_id, create_transaction,from app.schemas.schemas import Transaction as TransactionSchema, TransactionCreate, TransactionUpdate



@router.get("/", response_model=List[TransactionResponse])    update_transaction, delete_transaction, get_user_balance,from app.services.auth import get_current_user

def get_user_transactions(

    skip: int = Query(0, ge=0),    get_monthly_summary, get_recent_transactions

    limit: int = Query(100, ge=1, le=1000),

    start_date: Optional[datetime] = None,)router = APIRouter()

    end_date: Optional[datetime] = None,

    transaction_type: Optional[str] = None,from app.api.endpoints.auth import get_current_user

    category_id: Optional[int] = None,

    current_user = Depends(get_current_user),@router.get("/", response_model=List[TransactionSchema])

    db: Session = Depends(get_db)

):router = APIRouter(prefix="/transactions", tags=["transactions"])async def get_transactions(

    """Obter todas as transações do usuário"""

    return get_transactions_by_user(    skip: int = 0,

        db, current_user.id, skip, limit, 

        start_date, end_date, transaction_type, category_id@router.get("/", response_model=List[TransactionResponse])    limit: int = 100,

    )

def get_user_transactions(    db: Session = Depends(get_db),

@router.get("/recent", response_model=List[TransactionResponse])

def get_recent_user_transactions(    skip: int = Query(0, ge=0),    current_user = Depends(get_current_user)

    limit: int = Query(5, ge=1, le=50),

    current_user = Depends(get_current_user),    limit: int = Query(100, ge=1, le=1000),):

    db: Session = Depends(get_db)

):    start_date: Optional[datetime] = None,    """Buscar todas as transações do usuário"""

    """Obter as transações mais recentes"""

    return get_recent_transactions(db, current_user.id, limit)    end_date: Optional[datetime] = None,    transactions = db.query(Transaction).filter(



@router.get("/balance")    transaction_type: Optional[str] = None,        Transaction.user_id == current_user.id

def get_balance(

    current_user = Depends(get_current_user),    category_id: Optional[int] = None,    ).offset(skip).limit(limit).all()

    db: Session = Depends(get_db)

):    current_user = Depends(get_current_user),    return transactions

    """Obter saldo do usuário"""

    return get_user_balance(db, current_user.id)    db: Session = Depends(get_db)



@router.get("/summary/{year}/{month}")):@router.get("/{transaction_id}", response_model=TransactionSchema)

def get_summary(

    year: int,    """Obter todas as transações do usuário"""async def get_transaction(

    month: int,

    current_user = Depends(get_current_user),    return get_transactions_by_user(    transaction_id: int,

    db: Session = Depends(get_db)

):        db, current_user.id, skip, limit,     db: Session = Depends(get_db),

    """Obter resumo mensal"""

    if month < 1 or month > 12:        start_date, end_date, transaction_type, category_id    current_user = Depends(get_current_user)

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,    )):

            detail="Month must be between 1 and 12"

        )    """Buscar uma transação específica"""

    return get_monthly_summary(db, current_user.id, year, month)

@router.get("/recent", response_model=List[TransactionResponse])    transaction = db.query(Transaction).filter(

@router.get("/{transaction_id}", response_model=TransactionResponse)

def get_transaction(def get_recent_user_transactions(        Transaction.id == transaction_id,

    transaction_id: int,

    current_user = Depends(get_current_user),    limit: int = Query(5, ge=1, le=50),        Transaction.user_id == current_user.id

    db: Session = Depends(get_db)

):    current_user = Depends(get_current_user),    ).first()

    """Obter uma transação específica"""

    transaction = get_transaction_by_id(db, transaction_id, current_user.id)    db: Session = Depends(get_db)    

    if not transaction:

        raise HTTPException():    if not transaction:

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Transaction not found"    """Obter as transações mais recentes"""        raise HTTPException(status_code=404, detail="Transação não encontrada")

        )

    return transaction    return get_recent_transactions(db, current_user.id, limit)    



@router.post("/", response_model=TransactionResponse)    return transaction

def create_new_transaction(

    transaction: TransactionCreate,@router.get("/balance")

    current_user = Depends(get_current_user),

    db: Session = Depends(get_db)def get_balance(@router.post("/", response_model=TransactionSchema)

):

    """Criar uma nova transação"""    current_user = Depends(get_current_user),async def create_transaction(

    return create_transaction(db, transaction, current_user.id)

    db: Session = Depends(get_db)    transaction: TransactionCreate,

@router.put("/{transaction_id}", response_model=TransactionResponse)

def update_existing_transaction():    db: Session = Depends(get_db),

    transaction_id: int,

    transaction_update: TransactionUpdate,    """Obter saldo do usuário"""    current_user = Depends(get_current_user)

    current_user = Depends(get_current_user),

    db: Session = Depends(get_db)    return get_user_balance(db, current_user.id)):

):

    """Atualizar uma transação"""    """Criar uma nova transação"""

    transaction = update_transaction(db, transaction_id, transaction_update, current_user.id)

    if not transaction:@router.get("/summary/{year}/{month}")    # Verificar se a categoria existe e pertence ao usuário

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,def get_summary(    category = db.query(Category).filter(

            detail="Transaction not found"

        )    year: int,        Category.id == transaction.category_id,

    return transaction

    month: int,        Category.user_id == current_user.id

@router.delete("/{transaction_id}")

def delete_existing_transaction(    current_user = Depends(get_current_user),    ).first()

    transaction_id: int,

    current_user = Depends(get_current_user),    db: Session = Depends(get_db)    

    db: Session = Depends(get_db)

):):    if not category:

    """Deletar uma transação"""

    success = delete_transaction(db, transaction_id, current_user.id)    """Obter resumo mensal"""        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    if not success:

        raise HTTPException(    if month < 1 or month > 12:    

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Transaction not found"        raise HTTPException(    db_transaction = Transaction(

        )

    return {"message": "Transaction deleted successfully"}            status_code=status.HTTP_400_BAD_REQUEST,        **transaction.dict(),

            detail="Month must be between 1 and 12"        user_id=current_user.id

        )    )

    return get_monthly_summary(db, current_user.id, year, month)    

    db.add(db_transaction)

@router.get("/{transaction_id}", response_model=TransactionResponse)    db.commit()

def get_transaction(    db.refresh(db_transaction)

    transaction_id: int,    

    current_user = Depends(get_current_user),    return db_transaction

    db: Session = Depends(get_db)

):@router.put("/{transaction_id}", response_model=TransactionSchema)

    """Obter uma transação específica"""async def update_transaction(

    transaction = get_transaction_by_id(db, transaction_id, current_user.id)    transaction_id: int,

    if not transaction:    transaction_update: TransactionUpdate,

        raise HTTPException(    db: Session = Depends(get_db),

            status_code=status.HTTP_404_NOT_FOUND,    current_user = Depends(get_current_user)

            detail="Transaction not found"):

        )    """Atualizar uma transação"""

    return transaction    db_transaction = db.query(Transaction).filter(

        Transaction.id == transaction_id,

@router.post("/", response_model=TransactionResponse)        Transaction.user_id == current_user.id

def create_new_transaction(    ).first()

    transaction: TransactionCreate,    

    current_user = Depends(get_current_user),    if not db_transaction:

    db: Session = Depends(get_db)        raise HTTPException(status_code=404, detail="Transação não encontrada")

):    

    """Criar uma nova transação"""    # Atualizar apenas os campos fornecidos

    return create_transaction(db, transaction, current_user.id)    update_data = transaction_update.dict(exclude_unset=True)

    for field, value in update_data.items():

@router.put("/{transaction_id}", response_model=TransactionResponse)        setattr(db_transaction, field, value)

def update_existing_transaction(    

    transaction_id: int,    db.commit()

    transaction_update: TransactionUpdate,    db.refresh(db_transaction)

    current_user = Depends(get_current_user),    

    db: Session = Depends(get_db)    return db_transaction

):

    """Atualizar uma transação"""@router.delete("/{transaction_id}")

    transaction = update_transaction(db, transaction_id, transaction_update, current_user.id)async def delete_transaction(

    if not transaction:    transaction_id: int,

        raise HTTPException(    db: Session = Depends(get_db),

            status_code=status.HTTP_404_NOT_FOUND,    current_user = Depends(get_current_user)

            detail="Transaction not found"):

        )    """Deletar uma transação"""

    return transaction    db_transaction = db.query(Transaction).filter(

        Transaction.id == transaction_id,

@router.delete("/{transaction_id}")        Transaction.user_id == current_user.id

def delete_existing_transaction(    ).first()

    transaction_id: int,    

    current_user = Depends(get_current_user),    if not db_transaction:

    db: Session = Depends(get_db)        raise HTTPException(status_code=404, detail="Transação não encontrada")

):    

    """Deletar uma transação"""    db.delete(db_transaction)

    success = delete_transaction(db, transaction_id, current_user.id)    db.commit()

    if not success:    

        raise HTTPException(    return {"message": "Transação deletada com sucesso"}

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Transaction not found"@router.get("/filter/by-period")

        )async def get_transactions_by_period(

    return {"message": "Transaction deleted successfully"}    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Buscar transações por período"""
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    
    return transactions