from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel


app = FastAPI()

accounts = [
    {
        'account_id': 1,
        'account_name': 'Поездка в Москву',
        'account_type': 'Накопительный',
        'account_balance': 0,
        'currency': 'RUB'
    },
    {
        'account_id': 2,
        'account_name': 'Тинькофф Black',
        'account_type': 'Банковская карта',
        'account_balance': 15000,
        'currency': 'RUB'
    }
]


@app.get("/accounts", summary='Получить все счета', tags=['Финансы'])
def get_accounts():
    return accounts


@app.get("/accounts/{account_id}", summary='Получить информацию о счете', tags=['Финансы'])
def get_account(account_id: int):
    for account in accounts:
        if account_id == account["account_id"]:
            return account
    raise HTTPException(status_code=404, detail='Счет не найден')


class NewAccount(BaseModel):
    account_name: str
    account_type: str
    account_balance: int
    currency: str


@app.post("/accounts", summary='Добавить новый счет', tags=['Финансы'])
def create_book(new_account: NewAccount):
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
