from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create order from cart items"""
    # Get cart items
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Verify stock availability and calculate total
    total_amount = 0
    order_items_data = []
    
    for cart_item in cart_items:
        product = cart_item.product
        
        if not product.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"Product '{product.name}' is no longer available"
            )
        
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product '{product.name}'"
            )
        
        total_amount += product.price * cart_item.quantity
        order_items_data.append({
            "product_id": product.id,
            "quantity": cart_item.quantity,
            "price": product.price
        })
    
    # Create order
    db_order = models.Order(
        user_id=current_user.id,
        total_amount=total_amount,
        shipping_address=order.shipping_address,
        status="pending"
    )
    db.add(db_order)
    db.flush()  # Get order ID
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = models.OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(order_item)
        
        # Update product stock
        product = db.query(models.Product).filter(
            models.Product.id == item_data["product_id"]
        ).first()
        product.stock -= item_data["quantity"]
    
    # Clear cart
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).delete()
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[schemas.Order])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get user's orders"""
    orders = db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.get("/all", response_model=List[schemas.Order])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Get all orders (Admin only)"""
    orders = db.query(models.Order).order_by(
        models.Order.created_at.desc()
    ).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get specific order"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Users can only view their own orders, admins can view all
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order

@router.put("/{order_id}/status", response_model=schemas.Order)
def update_order_status(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Update order status (Admin only)"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = order_update.status
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Cancel order (only if status is pending)"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Users can only cancel their own orders
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this order")
    
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Can only cancel pending orders")
    
    # Restore stock
    for order_item in order.order_items:
        product = db.query(models.Product).filter(
            models.Product.id == order_item.product_id
        ).first()
        if product:
            product.stock += order_item.quantity
    
    order.status = "cancelled"
    db.commit()
    return None
