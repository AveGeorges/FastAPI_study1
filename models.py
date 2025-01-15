from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserSchema(BaseModel):
   user_name: str = Field(max_length=50)
   user_password: str = Field(max_length=50)
   email: EmailStr = Field(max_length=50)

   # model_config = ConfigDict(extra='forbid') # запретить доп поля, которые может внести пользователь
   
   
class AccountSchema(BaseModel):
   account_name: str = Field(max_length=50)
   account_type: str
   account_balance: int = Field(ge=0)
   currency: str = Field(max_length=50)
    
   # model_config = ConfigDict(extra='forbid')