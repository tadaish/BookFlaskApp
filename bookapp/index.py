import math

from flask import render_template, request, redirect
from bookapp import app, login, dao
from flask_login import login_user


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    books = dao.load_books(q=q, cate_id=cate_id, page=page)
    count = dao.get_count()

    return render_template('index.html', books=books, pages=math.ceil(count[1] / app.config['PAGE_SIZE']))


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/admin-login", methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories(),
    }


@app.route('/books/<int:id>')
def details(id):
    book = dao.get_book_by_id(id)
    return render_template('book-detail.html', book=book)


if __name__ == "__main__":
    with app.app_context():
        from bookapp import admin

        app.run(debug=True)
