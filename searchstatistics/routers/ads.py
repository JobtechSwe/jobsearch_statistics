from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date, datetime

from searchstatistics.repository import elastic

router = APIRouter()


class DateBucket(BaseModel):
    date: int
    count: int


class TermBucket(BaseModel):
    key: str
    count: int


@router.get("/ad/{ad_id}/views", response_model=List[DateBucket], tags=['ads'])
def ad_views(ad_id: int, from_date: date, to_date: date = datetime.now().date()):
    views = elastic.ad_views(ad_id, from_date, to_date)
    return views


@router.get("/ad/{ad_id}/terms", response_model=List[TermBucket], tags=['ads'])
def ad_freetext_terms(ad_id: int,
                      from_date: date,
                      to_date: date = datetime.now().date(),
                      n: int = 10):
    terms = elastic.ad_freetext_terms(ad_id, from_date, to_date, n)
    return terms
