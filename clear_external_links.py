from App import app
from Models import ProductModel
from extensions import db

with app.app_context():
    # Clear all placeholder external links
    products = ProductModel.query.all()
    
    for product in products:
        product.external_link = None
    
    db.session.commit()
    print(f"✅ Cleared external links from {len(products)} products!")
    print("\nNote: Sellers can now add real Amazon/Flipkart product links when listing products.")
