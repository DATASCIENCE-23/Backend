from passlib.context import CryptContext
from .repository import UserRepository
from .models import User
from .schemas import UserCreate, UserUpdate

# ✅ SAFE FOR PYTHON 3.13 (NO bcrypt)
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: UserCreate):
        hashed_password = pwd_context.hash(data.password)

        user = User(
            username=data.username,
            email=data.email,
            password=hashed_password,
            role=data.role
        )
        return self.repository.create(user)

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def get_all_users(self):
        return self.repository.get_all()

    def update_user(self, user_id: int, data: UserUpdate):
        update_data = data.dict(exclude_unset=True)  # convert to dict and skip unset fields
        return self.repository.update(user_id, update_data)


    def delete_user(self, user_id: int):
        return self.repository.delete(user_id)
