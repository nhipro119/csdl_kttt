from dataclasses import dataclass
from collections import Counter
from tool.analysis import analysis
@dataclass
class Abstract:
    """Wikipedia abstract"""
    ID: int
    title: str
    abstract: str
    url: str

    @property
    def fulltext(self):
        return ' '.join([self.title, self.abstract])
    def analyze(self):
            self.term_frequencies = Counter(analysis(self.fulltext))

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)