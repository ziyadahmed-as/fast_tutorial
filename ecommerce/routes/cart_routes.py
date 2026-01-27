from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

@router.post("/items", response_model=schemas.CartItem, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Add item to cart"""
    # Verify product exists and has enough stock
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.is_active:
        raise HTTPException(status_code=400, detail="Product is not available")
    
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    # Check if item already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += item.quantity
        if product.stock < existing_item.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Create new cart item
    db_item = models.CartItem(
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=schemas.CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get user's cart"""
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return {"items": cart_items, "total": total}

@router.put("/items/{item_id}", response_model=schemas.CartItem)
def update_cart_item(
    item_id: int,
    item_update: schemas.CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Update cart item quantity"""
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check stock availability
    if cart_item.product.stock < item_update.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    cart_item.quantity = item_update.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Remove item from cart"""
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return None

@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Clear all items from cart"""
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).delete()
    db.commit()
    return None
