from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from bookapp.models import Category, Book, UserRole, User, Receipt, ReceiptDetails
from bookapp import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class BookView(AuthenticatedView):
    column_list = ['id', 'title', 'category_id', 'author', 'price', 'year', 'count']
    column_searchable_list = ['id', 'title']
    column_filters = ['id', 'title', 'price']
    column_editable_list = ['title', 'price']
    can_export = True
    column_labels = {
        'title': 'Tên sách',
        'category_id': 'Thể loại',
        'author': 'Tác giả',
        'price': 'Giá',
        'year': 'Năm XB',
        'count': 'Số lượng'
    }


class CategoryView(AuthenticatedView):
    column_list = ['id', 'name', 'books']
    column_searchable_list = ['id', 'name']
    column_labels = {
        'name': 'Thể loại',
        'books': 'Sách'
    }


class UserView(AuthenticatedView):
    column_list = ['id', 'fullname', 'username', 'password', 'user_role']
    column_searchable_list = ['id', 'fullname', 'username']
    column_labels = {
        'fullname': 'Họ tên',
        'username': 'Tên tài khoản',
        'password': 'Mật khẩu',
        'user_role': 'Vài trò'
    }


class ReceiptView(AuthenticatedView):
    column_list = ['id', 'user_id', 'Tổng tiền', 'active', 'created_date']

    def total_amount_formatter(view, context, model, name):
        total = sum(item.quantity * item.unit_price for item in model.details)
        return f"{total:,.0f} đ"

    def user_fullname_formatter(view, context, model, name):
        return model.user.fullname

    column_formatters = {
        'user_id': user_fullname_formatter,
        'Tổng tiền': total_amount_formatter
    }

    column_labels = {
        'user_id': 'Tên khách hàng',
        'active': 'Trạng thái',
        'created_date': 'Ngày tạo',
    }


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_books_by_cate()
        revenue_by_cate = dao.get_revenue_by_cate()
        count = dao.get_count()
        return self.render('admin/index.html', stats=stats, count=count, rev_cat=revenue_by_cate)


admin = Admin(app, name='Book Administrators', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(CategoryView(Category, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
