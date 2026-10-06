from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.base import utcnow
from app.models.product import Product, ProductStatus
from app.schemas.product import ProductCreate, ProductList, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=ProductList)
def list_products(
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    status: ProductStatus | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    query = select(Product)
    count_query = select(func.count(Product.id))

    conditions = []
    if search:
        like = f"%{search}%"
        conditions.append(or_(Product.name.ilike(like), Product.sku.ilike(like)))
    if category_id is not None:
        conditions.append(Product.category_id == category_id)
    if status is not None:
        conditions.append(Product.status == status)

    for condition in conditions:
        query = query.where(condition)
        count_query = count_query.where(condition)

    total = session.exec(count_query).one()
    items = session.exec(query.order_by(Product.name).offset(offset).limit(limit)).all()
    return ProductList(items=items, total=total, limit=limit, offset=offset)


@router.post("/", response_model=ProductRead, status_code=201)
def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    product = Product.model_validate(data)
    if product.entry_date is None:
        from datetime import date

        product.entry_date = date.today()
    session.add(product)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(400, "El SKU ya existe")
    session.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    product.updated_at = utcnow()
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    session.delete(product)
    session.commit()
