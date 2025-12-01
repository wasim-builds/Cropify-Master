from flask import Blueprint, render_template, session, redirect, url_for, flash
from Models import UserModel, QueryModel, OrderModel
from extensions import db

admin = Blueprint('admin', __name__)

# Middleware to check if user is admin
def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash("Access Denied: Admins only!", "danger")
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin.route('/admin-dashboard')
@admin_required
def dashboard():
    # Fetch counts
    user_count = UserModel.query.count()
    order_count = OrderModel.query.count()
    query_count = QueryModel.query.count()
    
    # Fetch data
    users = UserModel.query.all()
    queries = QueryModel.query.all()

    return render_template('admin/dashboard.html', 
                           user_count=user_count, 
                           order_count=order_count, 
                           query_count=query_count,
                           users=users,
                           queries=queries)