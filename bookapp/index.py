import math

import cloudinary.uploader
from flask import render_template, request, redirect, jsonify, session
from bookapp import app, login, dao, utils
from flask_login import login_user, logout_user, login_required
from bookapp.models import UserRole
from bookapp.decorators import loggedin


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')
    order = request.args.get('order')
    books = dao.load_books(q=q, cate_id=cate_id, page=page, order=order)
    count = dao.get_count()

    return render_template('index.html', books=books, pages=math.ceil(count[1] / app.config['PAGE_SIZE']), page=page)


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
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@app.route('/books/<int:id>')
def details(id):
    book = dao.get_book_by_id(id)
    comments = dao.get_comments(id)
    return render_template('book-detail.html', book=book, comments=comments)


@app.route('/login', methods=['post', 'get'])
def login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            if user.user_role != UserRole.ADMIN:
                login_user(user)
            else:
                return redirect('/admin')

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


@app.route('/register', methods=['post', 'get'])
@loggedin
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_pass')
        if password.__eq__(confirm_pass):
            avatar_path = None
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']
            dao.add_user(fullname=request.form.get('name'),
                         username=request.form.get('username'),
                         password=request.form.get('password'),
                         email=request.form.get('email'),
                         phone=request.form.get('phone'),
                         address=request.form.get('address'),
                         avatar=avatar_path
                         )
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp'

    return render_template('register.html', err_msg=err_msg)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    if id in cart:
        cart[id]["quantity"] += request.json['quantity']
    else:
        cart[id] = {
            "id": id,
            "title": request.json.get("title"),
            "price": request.json.get("price"),
            "quantity": request.json.get('quantity'),
            "image": request.json.get("image")
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<book_id>', methods=['put'])
def update_cart(book_id):
    cart = session.get('cart')
    if cart and book_id in cart:
        cart[book_id]['quantity'] = request.json['quantity']
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<book_id>', methods=['delete'])
def delete_cart(book_id):
    cart = session.get('cart')
    if cart and book_id in cart:
        del cart[book_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/pay')
def pay_index():
    return render_template('pay.html')


@app.route("/api/pay", methods=['post'])
@login_required
def pay():
    cart = session.get('cart')
    try:
        dao.add_receipt(cart)
        for k, v in cart.items():
            dao.update_book_quantity(k, v['quantity'])
    except Exception as ex:
        print(ex)
        return jsonify({'status': 500})
    else:
        del session['cart']
        return jsonify({'status': 200})


@app.route('/api/books/<int:id>/comments', methods=['post'])
def add_comment(id):
    data = request.json
    c = dao.add_comment(content=data.get('content'), book_id=id)

    return jsonify({'status': 200})


@app.route('/user/user-info')
def user_info():
    return render_template('user-info.html')


@app.route('/user/user-receipt')
def user_receipt():
    receipts = dao.get_receipt_by_current_user()
    return render_template('user-receipt.html', receipts=receipts)


@app.route('/update-user', methods=['post'])
def update_user():
    username = request.form.get('username')
    fullname = request.form.get('fullname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    dao.update_user(fullname=fullname, username=username, phone=phone, email=email, address=address)

    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        from bookapp import admin

        app.run(debug=True)
