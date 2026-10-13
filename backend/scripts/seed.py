"""Poblar la base de datos con datos de demostración.

Uso (dentro del contenedor backend):
    python -m scripts.seed [num_productos]

Por defecto inserta 100 categorías/ proveedores mínimos y 1000 productos.
"""
import random
import sys
from datetime import date, timedelta

from sqlmodel import Session

from app.db.session import engine
from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier

CATS = [
    ("Lácteos", "Productos refrigerados"), ("Panadería", "Pan y repostería"),
    ("Bebidas", "Líquidos y refrescos"), ("Abarrotes", "Secos y enlatados"),
    ("Limpieza", "Artículos de aseo"), ("Enlatados", "Conservas"),
    ("Congelados", "Productos fríos"), ("Higiene", "Cuidado personal"),
]

SUPPLIERS = [
    ("Distribuidora Andina", "Carlos Pérez", "andina@example.com", "6015551234", "Cra 10 #20-30"),
    ("Alimentos del Valle", "Ana Gómez", "valle@example.com", "6025559876", "Av 5 #8-12"),
    ("Proveedora Central", "Luis Ruiz", "central@example.com", "6015554321", "Calle 15 #3-45"),
    ("Mercados S.A.S", "María Torres", "mercados@example.com", "6045556789", "Transversal 8 #10-22"),
]

ADJ = ["Premium", "Clásico", "Orgánico", "Familiar", "Económico", "Gourmet", "Tradicional", "Sin azúcar", "Natural", "Integral"]
PRODS = ["Leche", "Yogur", "Queso", "Pan", "Café", "Arroz", "Frijoles", "Aceite", "Azúcar", "Sal", "Agua", "Jugo",
         "Gaseosa", "Jabón", "Detergente", "Pasta", "Atún", "Sardinas", "Mantequilla", "Galletas", "Avena",
         "Harina", "Chocolate", "Té", "Miel", "Mermelada", "Cereal", "Pollo", "Carne", "Huevos", "Papa", "Cebolla"]
SIZES = ["500g", "1kg", "1L", "250ml", "Pack x6", "500ml", "2L", "400g"]


def main(n: int = 1000) -> None:
    random.seed(42)
    today = date.today()
    with Session(engine) as session:
        existing = {c.name for c in session.query(Category).all()}
        cats = [Category(name=n_, description=d) for n_, d in CATS if n_ not in existing]
        session.add_all(cats)
        existing_sup = {s.name for s in session.query(Supplier).all()}
        sups = [Supplier(name=n_, contact_name=c, email=e, phone=p, address=a) for n_, c, e, p, a in SUPPLIERS if n_ not in existing_sup]
        session.add_all(sups)
        session.commit()

        all_cats = session.query(Category).all()
        all_sups = session.query(Supplier).all()
        start = session.query(Product).count() + 1

        for i in range(start, start + n):
            expiry = None
            r = random.random()
            if 0.30 <= r < 0.50:
                expiry = today + timedelta(days=random.randint(0, 30))
            elif 0.50 <= r < 0.85:
                expiry = today + timedelta(days=random.randint(31, 365))
            qty = random.randint(0, 500)
            pp = round(random.uniform(0.5, 20), 2)
            session.add(Product(
                sku=f"SKU-{i:04d}",
                name=f"{random.choice(PRODS)} {random.choice(ADJ)} {random.choice(SIZES)}",
                category_id=random.choice(all_cats).id,
                supplier_id=random.choice(all_sups).id,
                quantity=qty,
                min_stock=random.choice([5, 10, 20, 50]),
                purchase_price=pp,
                sale_price=round(pp * random.uniform(1.2, 2.0), 2),
                entry_date=today - timedelta(days=random.randint(0, 365)),
                expiration_date=expiry,
                location=f"Estante {random.randint(1, 10)}-{random.randint(1, 5)}",
            ))
        session.commit()
        print(f"Seed completado: {len(cats)} categorías, {len(sups)} proveedores, {n} productos.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)
