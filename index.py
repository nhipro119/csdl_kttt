from tool.analysis import analysis
import math
class Index():
    #init function######
    def __init__(self):
        self.documents = {}
        self.index = {}
    #check and add document to list
    def index_document(self,document):
        if document.ID not in self.documents:
            self.documents[document.ID] = document
            document.analyze()
        for token in analysis(document.fulltext):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.ID)
    def document_frequency(self, token):
        return len(self.index.get(token, set()))
    # tokenlization document
    def inverse_document_frequency(self, token):
        # Manning, Hinrich and Schütze use log10, so we do too, even though it
        # doesn't really matter which log we use anyway
        # https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html
        return math.log10(len(self.documents) / self.document_frequency(token))

    def _results(self, analyzed_query):
        return [self.index.get(token, set()) for token in analyzed_query]