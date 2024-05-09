from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from bookapp.models import Category, Book, UserRole
from bookapp import app, db
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime


class MyBookView(ModelView):
    column_list = ['id', 'title', 'category_id', 'author', 'price', 'year']
    column_searchable_list = ['id', 'title']
    column_filters = ['id', 'title', 'price']
    column_editable_list = ['title', 'price']
    can_export = True
    column_labels = {
        'title': 'Tên sách',
        'category_id': 'Thể loại',
        'author': 'Tác giả',
        'price': 'Giá',
        'year': 'Năm XB'
    }


class MyCategoryView(ModelView):
    column_list = ['id', 'name', 'books']


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


# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         stats = dao.count_products_by_cate()
#         return self.render('admin/index.html', stats=stats)


admin = Admin(app, name='E-commerce Website', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyBookView(Book, db.session))
# admin.add_view(StatsView(name='Thống kê'))
# admin.add_view(LogoutView(name='Đăng xuất'))
