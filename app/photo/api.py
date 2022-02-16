from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header




from app.db.db import DB

photo_router = APIRouter(tags=["Photo"])


#@photo_router.post('/product/photo')
#async def add_photo(product_id: Optional[int] = Header(None,description='Id продукта'),

   