from fastapi import APIRouter, Query
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
def ad_count_taxonomy_field(
        limit: int = 21,
        filter_by: str = Query(
            None, name="filter", title="Concept ID filter",
            description="Filter results by concept ID for region or municipality")):
    views = elastic.taxonomy_code_count(concept_type="occupation_field.concept_id.keyword",
                                        filter_by=filter_by,
                                        filter_fields=[
                                            "workplace_address.region_code",
                                            "workplace_address.region_concept_id",
                                            "workplace_address.municipality_code",
                                            "workplace_address.municipality_concept_id"
                                        ], n=limit)
    return views


@router.get("/adcount/occupation-group",
            response_model=List[AdCountBucket], tags=['stats'])
def ad_count_taxonomy_group(
        field_concept_id: str,
        limit: int = 50,
        filter_by: str = Query(
            None, name="filter", title="Concept ID filter",
            description="Filter results by concept ID for region or municipality")):
    views = elastic.taxonomy_code_count(concept_type="occupation_group.concept_id.keyword",
                                        parent_fields=["occupation_field.concept_id.keyword"],
                                        parent_concept_id=field_concept_id,
                                        filter_fields=[
                                            "workplace_address.region_code",
                                            "workplace_address.region_concept_id",
                                            "workplace_address.municipality_code",
                                            "workplace_address.municipality_concept_id"
                                        ], filter_by=filter_by, n=limit)
    return views


@router.get("/adcount/occupation-name",
            response_model=List[AdCountBucket], tags=['stats'])
def ad_count_taxonomy_occupation(group_concept_id: str, limit: int = 50,
                                 filter_by: str = Query(
                                    None, name="filter", title="Concept ID filter",
                                    description="Filter results by concept ID for region or municipality")):
    views = elastic.taxonomy_code_count(concept_type="occupation.concept_id.keyword",
                                        parent_fields=["occupation_group.concept_id.keyword"],
                                        parent_concept_id=group_concept_id,
                                        filter_fields=[
                                            "workplace_address.region_code",
                                            "workplace_address.region_concept_id",
                                            "workplace_address.municipality_code",
                                            "workplace_address.municipality_concept_id"
                                        ], filter_by=filter_by, n=limit)
    return views


@router.get("/adcount/municipality",
            response_model=List[AdCountBucket], tags=['stats'])
# Default limit to maximum number of municipalities by region
def ad_count_municipality(
        region_code: str, limit: int = 49,
        filter_by: str = Query(None, name="filter", title="Concept ID filter",
                               description="Filter results by concept ID for occupation, group or field")):
    views = elastic.taxonomy_code_count(concept_type="workplace_address.municipality_concept_id",
                                        parent_fields=["workplace_address.region_code",
                                                       "workplace_address.region_concept_id"],
                                        parent_concept_id=region_code, filter_by=filter_by,
                                        filter_fields=[
                                            "occupation.concept_id.keyword",
                                            "occupation_group.concept_id.keyword",
                                            "occupation_field.concept_id.keyword"
                                        ], n=limit)
    return views


@router.get("/adcount/region",
            response_model=List[AdCountBucket], tags=['stats'])
def ad_count_region(
        limit: int = 21,
        filter_by: str = Query(None, name="filter", title="Concept ID filter",
                               description="Filter results by concept ID for occupation, group or field")):

    views = elastic.taxonomy_code_count(concept_type="workplace_address.region_concept_id",
                                        filter_by=filter_by,
                                        filter_fields=[
                                            "occupation.concept_id.keyword",
                                            "occupation_group.concept_id.keyword",
                                            "occupation_field.concept_id.keyword"
                                        ], n=limit)
    return views
