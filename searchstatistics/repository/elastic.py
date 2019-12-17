from functools import lru_cache

from elasticsearch import Elasticsearch
import certifi
import time
import json
from ssl import create_default_context
from searchstatistics import settings


if settings.ES_USER and settings.ES_PWD:
    context = create_default_context(cafile=certifi.where())
    elastic = Elasticsearch([settings.ES_HOST], port=settings.ES_PORT,
                            use_ssl=True, scheme='https',
                            ssl_context=context,
                            http_auth=(settings.ES_USER, settings.ES_PWD))
else:
    elastic = Elasticsearch([{'host': settings.ES_HOST, 'port': settings.ES_PORT}])


def ad_views(ad_id, from_date, to_date, interval='d'):
    dsl = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"returned_ads": ad_id}},
                    {"range": {"timestamp": {"gte": from_date}}},
                    {"range": {"timestamp": {"lte": to_date}}}
                ]
            }
        },
        "aggs": {
            "ad_hits": {
                "date_histogram": {
                    "field": "timestamp",
                    "interval": "1" + interval
                }
            }
        }
    }
    views = elastic.search(index=settings.ES_INDEX, body=dsl)
    return [{"date": b['key'], "count": b['doc_count']}
            for b in views['aggregations']['ad_hits']['buckets']]


def ad_freetext_terms(ad_id, from_date, to_date, n):
    dsl = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"returned_ads": ad_id}},
                    {"range": {"timestamp": {"gte": from_date}}},
                    {"range": {"timestamp": {"lte": to_date}}}
                ]
            }
        },
        "aggs": {
            "ad_freetext_terms": {
                "terms": {
                    "field": "q_keywords.keyword",
                    "size": n
                }
            }
        }
    }
    freetext_terms = elastic.search(index=settings.ES_INDEX, body=dsl)
    return [{"key": f['key'], "count": f['doc_count']}
            for f in freetext_terms['aggregations']['ad_freetext_terms']['buckets']]


def taxonomy_code_count(concept_type, parent_fields=None,
                        parent_concept_id=None, n=10000):
    offset = _calculate_utc_offset()
    dsl = {
        'size': 0,
        'query': {
            'bool': {
                'filter': [
                    {
                        'range': {
                            'publication_date': {
                                'lte': 'now+%dH/m' % offset
                            }
                        }
                    },
                    {
                        'range': {
                            'last_publication_date': {
                                'gte': 'now+%dH/m' % offset
                            }
                        }
                    },
                    {
                        'term': {
                            'removed': False
                        }
                    },
                ]
            }
        },
        'aggs': {
            'ad_count': {
                'terms': {
                    'field': concept_type,
                    'size': n
                }
            }
        }
    }
    if parent_concept_id and parent_fields:
        alternatives = []
        for parent_field in parent_fields:
            alternatives.append({'term': {parent_field: parent_concept_id}})
        dsl['query']['bool']['must'] = {
            'bool': {'should': [alternatives]}
        }
    occurences = elastic.search(index=settings.ES_PLATSANNONS_INDEX, body=dsl)
    return [
        {
            "concept_id": o['key'],
            "count": o['doc_count'],
            "label": _get_taxonomy_label(o['key'])
        } for o in occurences['aggregations']['ad_count']['buckets']
    ]


@lru_cache(maxsize=8192)
def _get_taxonomy_label(concept_id):
    taxonomy_entity = elastic.get(index=settings.ES_TAXONOMY_INDEX, id=concept_id,
                                  _source=['label'])
    return taxonomy_entity.get('_source', {}).get('label')


def _calculate_utc_offset():
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset = - (time.altzone if is_dst else time.timezone)
    return int(utc_offset/3600) if utc_offset > 0 else 0
