import os
import re

from dotenv import load_dotenv
from elasticsearch import Elasticsearch


from logging_utils import get_logger

logger = get_logger(__name__)
load_dotenv()


BONSAI_URL = os.environ['BONSAI_URL']


def get_es_client():
    auth = re.search('https\:\/\/(.*)\@', BONSAI_URL).group(1).split(':')
    host = BONSAI_URL.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    match = re.search('(:\d+)', host)
    if match:
        p = match.group(0)
        host = host.replace(p, '')
        port = int(p.split(':')[1])
    else:
        port = 443

    # Connect to cluster over SSL using auth for best security:
    es_header = [{
        'host': host,
        'port': port,
        'use_ssl': True,
        'http_auth': (auth[0], auth[1])
    }]

    return Elasticsearch(es_header)


def delete_document_by_id(
        document_id: str,
        index: str
):
    """
    Deletes a document from the Elasticsearch database using the document id
    :param document_id:
    :param index:
    :return:
    """
    es = get_es_client()
    return es.delete(index=index, id=document_id)


def update_document_by_id(
        document_id,
        document_body: dict,
        index: str
):
    es = get_es_client()
    body = {
        "doc": {
            **document_body
        }
    }
    return es.update(index=index, id=document_id, body=body)

