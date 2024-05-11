from bookapp.models import User, Category, Book, Receipt
import hashlib
from sqlalchemy import func
from bookapp import app, db


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def count_books_by_cate():
    return db.session.query(Category.id, Category.name,
                            func.count(Book.id)).join(Book, Book.category_id.__eq__(Category.id),
                                                      isouter=True).group_by(Category.id).all()


def get_count():
    count = []
    total_cate = Category.query.count()
    total_book = Book.query.count()
    total_user = User.query.count()
    total_receipt = Receipt.query.count()

    count.extend((total_cate, total_book, total_user, total_receipt))

    return count


def load_categories():
    return Category.query.all()


def load_books(q=None, cate_id=None, page=None):
    query = Book.query

    if q:
        query = query.filter(Book.name.contains(q) or Book.author.contains(q))

    if cate_id:
        query = query.filter(Book.category_id.__eq__(cate_id))

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)

    return query.all()


def get_book_by_id(id):
    return Book.query.get(id)
