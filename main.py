from fastapi import FastAPI, HTTPException
import uvicorn

from data import accounts, users
from models import UserSchema, AccountSchema


app = FastAPI()


# users endpoints 
@app.post("/users", summary='Добавить нового пользователя', tags=['Пользователи'])
def add_user(new_user: UserSchema):
   users.append({
        "user_id": len(users) + 1,
        "user_name": new_user.account_name,
        "user_password": new_user.account_balance,
        "email": new_user.currency
    })
   return {"success": True, "message": "Пользователь успешно добавлен"}


@app.get("/users", summary='Добавить нового пользователя', tags=['Пользователи'])
def get_users() -> list[UserSchema]:
   return users


# accounts endpoints 
@app.get("/accounts", summary='Получить все счета', tags=['Финансы'])
def get_accounts() -> list[AccountSchema]: 
    return accounts


@app.get("/accounts/{account_id}", summary='Получить информацию о счете', tags=['Финансы'])
def get_account(account_id: int) -> AccountSchema:
    for account in accounts:
        if account_id == account["account_id"]:
            return account
    raise HTTPException(status_code=404, detail='Счет не найден')


@app.post("/accounts", summary='Добавить новый счет', tags=['Финансы'])
def add_account(new_account: AccountSchema):
    accounts.append({
        "account_id": len(accounts) + 1,
        "account_name": new_account.account_name,
        "account_type": new_account.account_type,
        "account_balance": new_account.account_balance,
        "currency": new_account.currency
    })
    return {"success": True, "message": "Книга успешно добавлена"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
