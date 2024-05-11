import math
from flask import render_template, request, redirect, jsonify
from bookapp import app, login, dao
from flask_login import login_user, logout_user, logged
from bookapp.models import UserRole


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
        'role': UserRole,
    }


@app.route('/books/<int:id>')
def details(id):
    book = dao.get_book_by_id(id)
    comments = dao.get_comments(id)
    return render_template('book-detail.html', book=book, comments=comments)


@app.route('/api/books/<int:id>/comments', methods=['post'])
def add_comment(id):
    data = request.json
    c = dao.add_comment(content=data.get('content'), book_id=id)

    return jsonify({'id': c.id, 'content': c.content, 'user': {
        'username': c.user.username,
        'avatar': c.user.avatar
    }})


@app.route('/login')
def login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            login_user(user)

            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = 'Tên tài khoản hoặc mật khẩu không đúng'
    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def logout():
    logout_user()
    next = request.args.get('next')
    return redirect(next if next else '/')


if __name__ == "__main__":
    with app.app_context():
        from bookapp import admin

        app.run(debug=True)
