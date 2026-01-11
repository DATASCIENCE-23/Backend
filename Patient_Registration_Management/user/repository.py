from sqlalchemy.orm import Session
from .models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_all(self):
        return self.db.query(User).all()

    def update(self, user_id: int, data):
        if hasattr(data, "dict"):       # check if it's a Pydantic model
            data = data.dict(exclude_unset=True)
    
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user
