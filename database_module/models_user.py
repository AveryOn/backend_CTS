from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from engine import BaseUsers

class User(BaseUsers):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    pet = relationship('Pet', back_populates="owner")

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r}, hashed_password={self.hashed_password!r}, is_active={self.is_active!r})"