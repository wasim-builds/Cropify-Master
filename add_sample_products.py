from App import app
from Models import ProductModel
from extensions import db
from datetime import datetime

with app.app_context():
    # Sample products for the agricultural marketplace
    products = [
        # Seeds Category
        ProductModel(
            name="Organic Tomato Seeds",
            description="Premium quality organic tomato seeds. High yield variety suitable for greenhouse and open field cultivation. Disease resistant and produces large, juicy tomatoes.",
            price=299,
            img_url="https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=500",
            category="Seeds",
            stock=150,
            rating=4.5,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Hybrid Corn Seeds",
            description="High-yielding hybrid corn seeds with excellent germination rate. Suitable for various soil types and climate conditions. Early maturing variety.",
            price=450,
            img_url="https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=500",
            category="Seeds",
            stock=200,
            rating=4.7,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Carrot Seeds Premium",
            description="Sweet and crunchy carrot variety. Rich in nutrients and perfect for home gardens. Includes planting instructions.",
            price=199,
            img_url="https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=500",
            category="Seeds",
            stock=120,
            rating=4.3,
            userId=1,
            time=datetime.now()
        ),
        
        # Fertilizers Category
        ProductModel(
            name="NPK Fertilizer 10-26-26",
            description="Balanced NPK fertilizer for all crops. Promotes healthy growth, strong roots, and increased yield. Water-soluble formula for easy application.",
            price=850,
            img_url="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=500",
            category="Fertilizers",
            stock=80,
            rating=4.6,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Organic Compost 25kg",
            description="100% organic compost made from decomposed plant materials. Enriches soil with nutrients and improves soil structure. Perfect for organic farming.",
            price=650,
            img_url="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500",
            category="Fertilizers",
            stock=100,
            rating=4.8,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Liquid Seaweed Fertilizer",
            description="Natural liquid fertilizer extracted from seaweed. Rich in micronutrients and growth hormones. Suitable for all crops and plants.",
            price=550,
            img_url="https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=500",
            category="Fertilizers",
            stock=60,
            rating=4.4,
            userId=1,
            time=datetime.now()
        ),
        
        # Pesticides Category
        ProductModel(
            name="Organic Neem Oil Spray",
            description="Natural pesticide made from neem oil. Effective against aphids, mites, and other common pests. Safe for beneficial insects when used correctly.",
            price=380,
            img_url="https://images.unsplash.com/photo-1585928350859-efd86fba2d42?w=500",
            category="Pesticides",
            stock=90,
            rating=4.5,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Bio-Insecticide Spray",
            description="Biological insecticide for controlling caterpillars and leaf-eating insects. Eco-friendly and safe for crops. No residue on harvested produce.",
            price=425,
            img_url="https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=500",
            category="Pesticides",
            stock=75,
            rating=4.2,
            userId=1,
            time=datetime.now()
        ),
        
        # Tools Category
        ProductModel(
            name="Professional Garden Hoe",
            description="Heavy-duty garden hoe with ergonomic wooden handle. Perfect for weeding, cultivating, and breaking up soil. Durable steel blade.",
            price=750,
            img_url="https://images.unsplash.com/photo-1617576683096-00fc8eecb3af?w=500",
            category="Tools",
            stock=45,
            rating=4.7,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Pruning Shears Set",
            description="Professional quality pruning shears with sharp stainless steel blades. Comfortable grip handles reduce hand fatigue. Includes storage pouch.",
            price=950,
            img_url="https://images.unsplash.com/photo-1617576683096-00fc8eecb3af?w=500",
            category="Tools",
            stock=55,
            rating=4.8,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Garden Fork Heavy Duty",
            description="4-prong garden fork made from tempered steel. Ideal for turning soil, mixing compost, and harvesting root vegetables. Long-lasting construction.",
            price=880,
            img_url="https://images.unsplash.com/photo-1617576683096-00fc8eecb3af?w=500",
            category="Tools",
            stock=40,
            rating=4.6,
            userId=1,
            time=datetime.now()
        ),
        
        # Equipment Category
        ProductModel(
            name="Garden Sprayer 16L",
            description="Backpack pressure sprayer with adjustable nozzle. Perfect for applying pesticides, fertilizers, and water. Durable tank with comfortable straps.",
            price=2500,
            img_url="https://images.unsplash.com/photo-1564951434112-64d74cc2a2d7?w=500",
            category="Equipment",
            stock=25,
            rating=4.5,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Electric Grass Trimmer",
            description="Lightweight electric grass trimmer for lawn edges and tight spaces. Adjustable height and angle. Low noise operation.",
            price=4200,
            img_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500",
            category="Equipment",
            stock=15,
            rating=4.4,
            userId=1,
            time=datetime.now()
        ),
        
        # Irrigation Category
        ProductModel(
            name="Drip Irrigation Kit 50m",
            description="Complete drip irrigation system for gardens up to 500 sq ft. Water-saving technology with adjustable drippers. Easy installation.",
            price=3200,
            img_url="https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=500",
            category="Irrigation",
            stock=30,
            rating=4.7,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Garden Hose 30m Premium",
            description="Flexible and durable garden hose with anti-kink technology. Includes spray nozzle with 7 patterns. UV resistant material.",
            price=1250,
            img_url="https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=500",
            category="Irrigation",
            stock=50,
            rating=4.3,
            userId=1,
            time=datetime.now()
        ),
        
        # Organic Products Category
        ProductModel(
            name="Vermicompost 10kg",
            description="Premium quality vermicompost produced from earthworms. Rich in nutrients and beneficial microorganisms. Improves soil health naturally.",
            price=450,
            img_url="https://images.unsplash.com/photo-1585928350859-efd86fba2d42?w=500",
            category="Organic Products",
            stock=70,
            rating=4.9,
            userId=1,
            time=datetime.now()
        ),
        ProductModel(
            name="Organic Pest Repellent",
            description="Natural pest repellent made from essential oils and plant extracts. Safe for humans, pets, and beneficial insects. Pleasant aroma.",
            price=320,
            img_url="https://images.unsplash.com/photo-1585928350859-efd86fba2d42?w=500",
            category="Organic Products",
            stock=85,
            rating=4.4,
            userId=1,
            time=datetime.now()
        ),
    ]
    
    # Add all products to the database
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    print(f"✅ Successfully added {len(products)} products to the marketplace!")
    print("\nProduct categories:")
    categories = {}
    for product in products:
        categories[product.category] = categories.get(product.category, 0) + 1
    
    for category, count in categories.items():
        print(f"  - {category}: {count} products")
