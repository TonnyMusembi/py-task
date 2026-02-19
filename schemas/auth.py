from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    role: str

class RefreshTokenInput(BaseModel):
    refresh_token: str

class resetPasswordInput(BaseModel):
    email: EmailStr
    new_password: str
