import dataclass
import load_data
import index
from pymilvus import MilvusClient, DataType
from pymilvus import utility
from tool import analysis
import json
client = MilvusClient(
    uri="http://localhost:19530"
)
client.drop_collection(collection_name="token")
client.drop_collection(collection_name="document")
document_schema = MilvusClient.create_schema(
    auto_id=False,
    enable_dynamic_field=True,
)
document_schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
document_schema.add_field(field_name="info", datatype=DataType.JSON)
document_schema.add_field(field_name="tf", datatype=DataType.JSON)
document_index_params = client.prepare_index_params()
document_index_params.add_index(
    field_name="id",
    index_type="STL_SORT"
)

client.create_collection(
    collection_name="document",
    schema=document_schema,
    index_params=document_index_params
)



index_schema = MilvusClient.create_schema(
    auto_id=False,
    enable_dynamic_field=True,
)
index_schema.add_field(field_name="id", datatype=DataType.VARCHAR,max_length=1000, is_primary=True)
index_schema.add_field(field_name="document_id", datatype=DataType.ARRAY,max_capacity=4096, element_type=DataType.INT64 )
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="id"
)
client.create_collection(
    collection_name="token",
    schema=index_schema,
    index_params=index_params
)


# res = client.list_collections()
# print(res)
def index_documents(load_documents, index):
    documents = load_data.load_DANeS()
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents')
        if i == 10000:
            break
    return index
if __name__ == "__main__":
    index = index_documents(1,index.Index())
    documents = index.documents
    
    ds = []
    
    for k in documents.keys():
        
        
        coutnter_tf = documents[k].term_frequencies
        tf = {}
        for key, value in coutnter_tf.items():
            tf[key] = value
        ds.append({"id":documents[k].ID,"info":{"title":documents[k].title,"abstract":documents[k].abstract,"url":documents[k].url},"tf":tf})
    res = client.insert(
    collection_name="document",
    data=ds
    )


    idx = index.index
    lidx = []
    for i in idx.keys():

        a = idx[i]
        lidx.append({"id":i,"document_id":a})
        if(len(a) >= 4000):
            print("maxx:")
            print([i])
            print(len(a))
    res = client.insert(
    collection_name="token",
    data=lidx
    )

    print(res)

