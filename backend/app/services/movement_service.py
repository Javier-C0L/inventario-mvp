from fastapi import HTTPException
from sqlmodel import Session

from app.models.movement import InventoryMovement, MovementType
from app.models.product import Product, ProductStatus


def register_movement(session: Session, product_id: int, movement_type: MovementType, quantity: int, note: str | None) -> InventoryMovement:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")

    previous = product.quantity
    if movement_type == MovementType.OUT and quantity > previous:
        raise HTTPException(400, f"Stock insuficiente: disponible {previous}, solicitado {quantity}")

    new_quantity = previous + quantity if movement_type == MovementType.IN else previous - quantity
    product.quantity = new_quantity
    if new_quantity == 0:
        product.status = ProductStatus.agotado.value
    elif movement_type == MovementType.IN and product.status == ProductStatus.agotado.value:
        product.status = ProductStatus.vigente.value

    movement = InventoryMovement(
        product_id=product_id,
        movement_type=movement_type.value,
        quantity=quantity,
        previous_quantity=previous,
        new_quantity=new_quantity,
        note=note,
    )
    session.add(product)
    session.add(movement)
    session.commit()
    session.refresh(movement)
    return movement
