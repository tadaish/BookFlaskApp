from enum import Enum as RoleEnum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin

from bookapp import db, app


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100))
    avatar = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0)
    description = Column(String(200))
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class Receipt(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(Base):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)


class Comment(Base):
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
