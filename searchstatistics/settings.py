import os

ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_USER = os.getenv("ES_USER")
ES_PWD = os.getenv("ES_PWD")

ES_INDEX = os.getenv("ES_INDEX", "search-events")
