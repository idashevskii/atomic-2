import logging
from qdrant_client.http import models

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

QDRANT_LOCATION = 'http://atomic2.open-core.ru'

COLL_NAME = 'rtm'

qdrant_client = QdrantClient(QDRANT_LOCATION, port=6333)

def make_sure_collection(coll_name, vec_size):
    if not qdrant_client.collection_exists(coll_name):
        qdrant_client.create_collection(coll_name,VectorParams(size=vec_size, distance=Distance.COSINE))

def list_files(coll_name)->list[str]:
    offset = None
    result = set()
    try:
        while True:
            recs, offset = qdrant_client.scroll(
                collection_name=coll_name,
                offset=offset,
                #scroll_filter=models.Filter(should=clauses),
                with_payload=True,
                with_vectors=False
            )
            for q in recs:
                result.add(q.payload['file'])
            if not offset:
                break
        result = sorted(result)
    except Exception as e:
        logging.error("unable to list %s", coll_name, e)
    return result
