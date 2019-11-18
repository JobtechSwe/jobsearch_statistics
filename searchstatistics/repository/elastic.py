from elasticsearch import Elasticsearch
import certifi
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
    return [{"date": b['key'], "count": b['doc_count']}for b in views['aggregations']['ad_hits']['buckets']]


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
    return [{"key": f['key'], "count": f['doc_count']} for f in freetext_terms['aggregations']['ad_freetext_terms']['buckets']]
