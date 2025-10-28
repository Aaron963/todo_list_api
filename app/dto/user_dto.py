from pydantic import BaseModel, Field, EmailStr, field_validator


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    full_name: str = Field(..., min_length=2, max_length=100)

    @field_validator('password')
    def password_must_contain_letter_and_number(cls, v):
        # Password must contain at least one letter and one number, and be at least 8 characters long.
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
