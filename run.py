import dataclass
import load_data
import index
from tool import analysis
def add_database():
    def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
        if i > 100000:
            break
    return index