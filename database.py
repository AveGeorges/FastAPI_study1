from typing import Annotated
from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# создается база данных и подключение к ней - сессию
engine = create_async_engine('sqlite+aiosqlite:///finances.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
   async with new_session() as session:
      yield session
      

# Создание инъекции зависсссмосстей - создание сесии
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
   pass


# описание таблицы через orm sqlalchemy для таблицы базы данных    
class FinancalTargetModel(Base):
   __tablename__ = 'targets'
   
   id: Mapped[int] = mapped_column(primary_key=True)
   target_name: Mapped[str]
   target_description: Mapped[str]
   target_balance: Mapped[int]
   target_purpose: Mapped[int]
   currency: Mapped[str]


# создание таблицы через orm sqlalchemy 
@app.post("/setup_database")
async def setup_database():
   async with engine.begin() as connection:
      await connection.run_sync(Base.metadata.drop_all)
      await connection.run_sync(Base.metadata.create_all) # в аттрибуте metadata хранятся все данные о полях, связях и т.д. в таблицах; create_all - создание схемы таблиц с полями
   return {"success": True}


# создание модели(схемы) для цели Target
class TargetAddSchema(BaseModel):
   target_name: str = Field(max_length=50)
   target_description: str = Field(max_length=200)
   target_balance: int
   target_purpose: int
   currency: str = Field(max_length=10)

class TargetSchema(TargetAddSchema):
   id: int


@app.post("/targets")
async def add_target(new_target: TargetSchema, session: SessionDep):
   # прокидываем через orm модель(FinancalTargetModel) поля из pydantiсс схемы (TargetAddSchema)
   new_target = FinancalTargetModel(
      target_name = new_target.target_name,
      target_description = new_target.target_description,
      target_balance = new_target.target_balance,
      target_purpose = new_target.target_purpose,
      currency = new_target.currency
   )
   # в сессию алхимии добавляем созданный объект для дальнейшего его добавления в бд
   session.add(new_target)
   # подтверждение транзакций сессии
   await session.commit()

   return {"success": True, "message": 'Финансовая цель успешно добавлена'}


@app.get("/targets")
async def get_targets(session: SessionDep):
   pass


if __name__ == "__main__":
    uvicorn.run("database:app", reload=True)