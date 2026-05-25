from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=10)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None 