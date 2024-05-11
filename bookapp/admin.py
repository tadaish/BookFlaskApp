from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from bookapp.models import Category, Book, UserRole, User
from bookapp import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime


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


# class StatsView(BaseView):
#     @expose('/')
#     def index(self):
#         revenue_by_prods = dao.stats_revenue_by_product(kw=request.args.get('kw'))
#         revenue_by_period = dao.stats_revenue_by_period(year=request.args.get('year', datetime.now().year),
#                                                         period=request.args.get('period', 'month'))
#
#         return self.render('admin/stats.html',
#                            revenue_by_prods=revenue_by_prods,
#                            revenue_by_period=revenue_by_period)
#
#     def is_accessible(self):
#         return current_user.is_authenticated


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
        count = dao.get_count()
        return self.render('admin/index.html', stats=stats, count=count)


admin = Admin(app, name='Book Administrators', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(CategoryView(Category, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
