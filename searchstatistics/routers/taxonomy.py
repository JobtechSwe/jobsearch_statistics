from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from searchstatistics.repository import elastic

router = APIRouter()


class AdCountBucket(BaseModel):
    concept_id: str
    label: str
    count: int


@router.get("/adcount/occupation-field",
            response_model=List[AdCountBucket], tags=['stats'])
def adcount_taxonomy_field():
    views = elastic.taxonomy_code_count("occupation_field.concept_id.keyword")
    return views


@router.get("/adcount/occupation-group",
            response_model=List[AdCountBucket], tags=['stats'])
def adcount_taxonomy_group(field_concept_id: str):
    views = elastic.taxonomy_code_count("occupation_group.concept_id.keyword",
                                        ["occupation_field.concept_id.keyword"],
                                        field_concept_id)
    return views


@router.get("/adcount/occupation-name",
            response_model=List[AdCountBucket], tags=['stats'])
def adcount_taxonomy_occupation(group_concept_id: str):
    views = elastic.taxonomy_code_count("occupation.concept_id.keyword",
                                        ["occupation_group.concept_id.keyword"],
                                        group_concept_id)
    return views


@router.get("/adcount/municipality",
            response_model=List[AdCountBucket], tags=['stats'])
def adcount_municipality(region_code: str):
    views = elastic.taxonomy_code_count("workplace_address.municipality_concept_id",
                                        ["workplace_address.region_code",
                                         "workplace_address.region_concept_id"],
                                        region_code)
    return views


@router.get("/adcount/region",
            response_model=List[AdCountBucket], tags=['stats'])
def adcount_region():
    views = elastic.taxonomy_code_count("workplace_address.region_concept_id")
    return views
