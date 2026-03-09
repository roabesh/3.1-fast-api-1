from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Advertisement
from app.schemas import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse

router = APIRouter(prefix="/advertisement", tags=["advertisements"])


@router.post("", response_model=AdvertisementResponse, status_code=201)
def create_advertisement(data: AdvertisementCreate, db: Session = Depends(get_db)):
    ad = Advertisement(**data.model_dump())
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


@router.get("/{advertisement_id}", response_model=AdvertisementResponse)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    ad = db.get(Advertisement, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@router.patch("/{advertisement_id}", response_model=AdvertisementResponse)
def update_advertisement(
    advertisement_id: int,
    data: AdvertisementUpdate,
    db: Session = Depends(get_db),
):
    ad = db.get(Advertisement, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ad, field, value)
    db.commit()
    db.refresh(ad)
    return ad


@router.delete("/{advertisement_id}", status_code=204)
def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    ad = db.get(Advertisement, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    db.delete(ad)
    db.commit()


@router.get("", response_model=List[AdvertisementResponse])
def search_advertisements(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Advertisement)
    if title:
        stmt = stmt.where(Advertisement.title.ilike(f"%{title}%"))
    if description:
        stmt = stmt.where(Advertisement.description.ilike(f"%{description}%"))
    if author:
        stmt = stmt.where(Advertisement.author.ilike(f"%{author}%"))
    if price_min is not None:
        stmt = stmt.where(Advertisement.price >= price_min)
    if price_max is not None:
        stmt = stmt.where(Advertisement.price <= price_max)
    return db.execute(stmt).scalars().all()
