from pydantic import BaseModel, EmailStr, Field, validator

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2, max_length=100)

    @validator("password")
    def password_strength(cls, v):
        if not (any(c.isalpha() for c in v) and any(c.isdigit() for c in v)):
            raise ValueError("Password must contain at least one letter and one number")
        return v

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponseDTO(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    class Config:
        orm_mode = True