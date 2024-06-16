# from transformers import logging
# logging.set_verbosity_error() # set_verbosity_warning()

import warnings
warnings.filterwarnings('ignore')

from sentence_transformers import SentenceTransformer
from sentence_transformers.models import Pooling, Transformer
from qdrant_client import QdrantClient
import requests

def get_bi_encoder(bi_encoder_name):
    raw_model = Transformer(model_name_or_path=bi_encoder_name)

    bi_encoder_dim = raw_model.get_word_embedding_dimension()

    pooling_model = Pooling(
        bi_encoder_dim,
        pooling_mode_cls_token = False,
        pooling_mode_mean_tokens = True
    )
    bi_encoder = SentenceTransformer(
        modules = [raw_model, pooling_model],
        device = 'cpu' # cuda DEVICE
    )

    return bi_encoder, bi_encoder_dim

# Формируем из строки вектор
def str_to_vec(bi_encoder, text):
    embeddings = bi_encoder.encode(
        text,
        convert_to_tensor = True,
        show_progress_bar = False
    )
    return embeddings


# Создаем подключение к векторной БД
qdrant_client = QdrantClient('atomic2.open-core.ru', port=6333)

def vec_search(bi_encoder, query, n_top_cos):
    # Кодируем запрос в вектор
    query_emb = str_to_vec(bi_encoder, query)

    # Поиск в БД
    search_result = qdrant_client.search(
        collection_name = COLL_NAME,
        query_vector = query_emb,
        limit = n_top_cos,
        with_vectors = False
    )

    top_chunks = [x.payload['chunk'] for x in search_result]
    top_files = list(set([x.payload['file'] for x in search_result]))

    return top_chunks, top_files

def get_rag_response(prompt):
    API_URL = "https://l4npxqyj15m9kzl5.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept" : "application/json",
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": prompt,
        "parameters": {
            "top_k": 150,
            "top_p": 0.20347480208997282,
            "temperature": 0.5954630385670282,
            "max_new_tokens": 726
        }
    })
    response = output[0]['generated_text'][len(prompt):]
    return response

COLL_NAME = 'rtm'

def get_rag_ans(query):
    COLL_NAME = 'rtm' 
    bi_encoder, vec_size = get_bi_encoder('BAAI/bge-m3')
    print('bi_encoder загружен')

    prompt_temp = '''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им.<|eot_id|><|start_header_id|>user<|end_header_id|>
    Используй только следующий контекст, чтобы кратко ответить на вопрос в конце. Если ответа не найден напиши "Ответ не найден". Не пытайся выдумывать ответ.
    Контекст:
    ###
    {chunks_join}
    ###
    Вопрос:
    ###
    {query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>'''

    top_chunks, top_files = vec_search(bi_encoder, query, 5)
    print('Запрос в кудрант')

    join_sym = '\n'
    chunks_join = join_sym.join(top_chunks)
    prompt = prompt_temp.format(chunks_join=chunks_join, query=query)
    ##print(prompt)
    respond = get_rag_response(prompt)

    return respond

    



