from bookapp.models import User, Category, Book, Receipt, Comment, ReceiptDetails
import hashlib
from sqlalchemy import func, desc
from bookapp import app, db
from flask_login import current_user


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
    total_revenue = db.session.query(func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)).scalar()

    count.extend((total_cate, total_book, total_user, total_receipt, total_revenue))

    return count


def load_categories():
    return Category.query.all()


def load_books(q=None, cate_id=None, page=None, order=None):
    query = Book.query.order_by(-Book.id)

    if q:
        query = query.filter(Book.title.contains(q))

    if cate_id:
        query = query.filter(Book.category_id.__eq__(cate_id))

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)

    if order:
        if order == 'best-selling':
            query = db.session.query(Book.id, Book.title, Book.price, Book.image,
                                     func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)
                                     ).join(Book, Book.id.__eq__(ReceiptDetails.book_id), isouter=True
                                            ).group_by(Book.id
                                                       ).order_by(
                func.sum(-ReceiptDetails.quantity * ReceiptDetails.unit_price))

        if order == 'min-price':
            query = Book.query.order_by(Book.price)

        if order == 'max-price':
            query = Book.query.order_by(-Book.price)

    return query.all()


def get_book_by_id(id):
    return Book.query.get(id)


def add_comment(content, book_id):
    c = Comment(content=content, book_id=book_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c


def get_comments(book_id):
    return Comment.query.filter(Comment.book_id.__eq__(book_id)).order_by(-Comment.id)


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               receipt=r, book_id=c['id'])
            db.session.add(d)

        db.session.commit()


def add_user(fullname, username, password, email, phone, address, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(fullname=fullname, username=username, password=password, email=email, phone=phone, address=address,
             avatar=avatar)
    db.session.add(u)
    db.session.commit()


def update_user(fullname, username, email, phone, address):
    current_user.fullname = fullname
    current_user.username = username
    current_user.email = email
    current_user.phone = phone
    current_user.address = address

    db.session.commit()


def get_receipt_by_current_user():
    return db.session.query(Receipt.id.label('id'),
                            User.fullname.label('name'),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label('total_amount'),
                            Receipt.created_date.label('created_date')
                            ).join(User, User.id.__eq__(Receipt.user_id)
                                   ).join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id)
                                          ).group_by(User.username, Receipt.id
                                                     ).filter(User.id.__eq__(current_user.id)).all()


def get_revenue_by_cate():
    return db.session.query(Category.id.label('cate_id'),
                            Category.name.label('cate_name'),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label('total_revenue')
                            ).join(Book, Book.category_id.__eq__(Category.id)
                                   ).join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Book.id)
                                          ).group_by('cate_id', 'cate_name').all()


def update_book_quantity(book_id, quantity):
    book = get_book_by_id(book_id)
    book.count -= quantity

    db.session.commit()
