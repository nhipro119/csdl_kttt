from query import Query
from tool import analysis
import math
class Application:
    def __init__(self):
        self.query = Query()
    def search(self,search_string):
        self.tokens = analysis.analysis(search_string)
        self.query_tokens_and_documents()
        result = self.rank_result()
        print(result)
        return result
        
        # print(idf)
        # self.tf(tokens=tokens, document_ids=self.document_ids)
    
    def query_tokens_and_documents(self):
        self.token_ids = self.query.token_query(self.tokens)
        ids = [set(token_id["document_id"]) for token_id in self.token_ids]
        ids = list(set.union(*ids))
        self.document_ids = self.query.document_query(ids)


    def rank_result(self):
        idfs = self.idf(self.token_ids)
        results = []
        for document_id in self.document_ids:
            score = 0.0
            for token in self.tokens:
                idf_score = idfs[token]
                tf_score = self.tf(token, document_id)
                score += idf_score*tf_score
            results.append([document_id["info"],score])
        return sorted(results, key=lambda doc: doc[1], reverse=True)
    
    
    def idf(self, token_ids):
        token_idfs = {}
        for token_id in token_ids:

            token_idfs[token_id["id"]] = math.log10(10002/len(token_id["document_id"]))

        return token_idfs
    def tf(self,token, document_id):

        doc_tf_list = document_id["tf"]
        return doc_tf_list.get(token, 0)


            
        
