from pymilvus import MilvusClient, DataType
from pymilvus import utility
class Query():
    def __init__(self):
        self.client = MilvusClient(
            uri="http://localhost:19530"
        )
    def document_query(self,ids):
        fil = "id in {}".format(ids)
        res = self.client.query(
            collection_name="document",
            # highlight-start
            filter=fil,
            output_fields=["id","info","tf"]
        )
        return res
    def token_query(self, tokens):
        fil = "id in {}".format(tokens)
        res = self.client.query(
            collection_name="token",
            filter=fil,
            # highlight-start
            output_fields=["id","document_id"]
            # highlight-end
        )
        return res