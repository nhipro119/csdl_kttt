from pyvi import ViTokenizer, ViPosTagger
print(ViTokenizer.tokenize(u"con chim cu hót líu lo, hót líu lo"))
print(ViPosTagger.postagging(ViTokenizer.tokenize(u"Trường đại học Bách Khoa Hà Nội\n")))
# import string
# import re
# PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))
# print(PUNCTUATION)