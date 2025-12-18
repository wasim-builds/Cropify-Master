from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from Models import OrderModel, ProductModel, UserModel
# CHANGE: Import from extensions, NOT from App (fixes circular import)
from extensions import db
import os

shop = Blueprint("shop", __name__)

# Product categories for farming marketplace
CATEGORIES = [
    'Seeds', 'Fertilizers', 'Pesticides', 'Tools', 
    'Equipment', 'Organic Products', 'Irrigation', 'General'
]

@shop.route("/add-product", methods=['GET', 'POST'])
def add_product():
    # check admin access
    if request.method == 'POST':
        name = request.form.get('p-name')
        price = request.form.get('p-price')
        des = request.form.get('des')
        category = request.form.get('category', 'General')
        stock = request.form.get('stock', 0)
        external_link = request.form.get('external_link', '').strip()

        product = ProductModel.query.filter_by(name=name).first()

        if product:
            flash("Product already exists", "danger")
            return redirect(url_for('shop.add_product'))

        file = request.files.get("img")
        if file:
            filename = 'static/images/products/'+secure_filename(file.filename)
            
            # Create directory if not exists
            os.makedirs('static/images/products', exist_ok=True)
            file.save(filename)
        else:
            filename = 'static/images/common/default-product.jpg'

        new_product = ProductModel(
            name=name,
            price=int(price),
            description=des,
            img_url=filename,
            category=category,
            stock=int(stock),
            external_link=external_link if external_link else None,
            userId=session.get('id')
        )

        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully", "success")
        return redirect(url_for('shop.all_products'))
        
    return render_template("shop/add-product.html", categories=CATEGORIES)

@shop.route("/all-products")
def all_products():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = ProductModel.query
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                ProductModel.name.like(search_term),
                ProductModel.description.like(search_term)
            )
        )
    
    products = query.order_by(ProductModel.time.desc()).all()
    
    # Get sellers info
    products_with_sellers = []
    for product in products:
        seller = UserModel.query.get(product.userId) if product.userId else None
        products_with_sellers.append((product, seller))

    return render_template("shop/all-products.html", 
                         products=products_with_sellers, 
                         categories=CATEGORIES,
                         selected_category=category)

@shop.route("/product-details")
def product_details():
    pid = request.args.get('pid')
    product = ProductModel.query.get(pid)
    
    if not product:
        flash("Product not found", "danger")
        return redirect(url_for('shop.all_products'))
    
    seller = UserModel.query.get(product.userId) if product.userId else None
    
    return render_template("shop/product-details.html", product=product, seller=seller)

@shop.route("/buy-product", methods=['GET', 'POST'])
def buy_product():
    if request.method == 'POST':
        pid = request.form.get('pid')
        quantity = int(request.form.get('quantity', 1))
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        product = ProductModel.query.get(pid)
        
        if not product:
            flash("Product not found", "danger")
            return redirect(url_for('shop.all_products'))
        
        if product.stock < quantity:
            flash(f"Only {product.stock} items available", "warning")
            return redirect(url_for('shop.product_details', pid=pid))
        
        total_price = product.price * quantity
        
        order = OrderModel(
            userId=session['id'], 
            productId=pid,
            quantity=quantity,
            total_price=total_price,
            address=address,
            phone=phone,
            status="Pending"
        )
        
        # Update stock
        product.stock -= quantity
        
        db.session.add(order)
        db.session.commit()

        flash("Order placed successfully!", "success")
        return redirect(url_for("shop.products"))
    
    # GET request - show order form
    pid = request.args.get('pid')
    product = ProductModel.query.get(pid)
    
    if not product:
        flash("Product not found", "danger")
        return redirect(url_for('shop.all_products'))
    
    return render_template("shop/checkout.html", product=product)

@shop.route("/orders")
def products():
    orders = OrderModel.query.filter_by(userId=session['id']).order_by(OrderModel.time.desc()).all()
    products = list()

    for order in orders:
        product = ProductModel.query.filter_by(id=order.productId).first()
        products.append((product, order))

    return render_template("shop/orders.html", products=products)