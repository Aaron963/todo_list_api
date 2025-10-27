from pydantic import BaseModel, EmailStr, Field, validator


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    full_name: str = Field(..., min_length=2, max_length=100)

    @validator("password")
    def password_strength(cls, v):
        # 密码必须包含至少一个字母、一个数字或特殊字符，并且长度至少为8位
        if not (any(c.isalpha() for c in v) and any(c.isdigit() for c in v) and len(v) >= 8):
            raise ValueError(
                "Password must contain at least one letter and one number, and be at least 8 characters long.")
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
        from_attributes = True
