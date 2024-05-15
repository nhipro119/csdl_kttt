from pyvi import ViTokenizer, ViPosTagger
import re
import string
PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))
stop_word_path = "IRS_Course-master/data/stopwords/vietnamese-stopwords.txt"
with open(stop_word_path,"r", encoding="utf-8") as f:
    stop_words = f.readlines()
    stop_words = [stop_word.replace("\n","") for stop_word in stop_words]
    stop_words = [stop_word.replace(" ","") for stop_word in stop_words]
def analysis(text):
    tokens = tokenlization(text)
    tokens = lowcase(tokens)
    tokens = pro_punctuation(tokens)
    tokens = stop_word(tokens)
    tokens = remove_empty(tokens)
    return tokens

def tokenlization(text):
    tokens = ViTokenizer.tokenize(text)
    tokens = tokens.split(" ")
    return tokens
def remove_empty(tokens):
    return [token for token in tokens if token != ""]
def lowcase(tokens):
    return [token.lower() for token in tokens ]
def pro_punctuation(tokens):
    return [PUNCTUATION.sub("", token) for token in tokens]
### stop world#####
def stop_word(tokens):
    return [token for token in tokens if token not in stop_words]

# with open("IRS_Course-master\\data\\vnexpress\\giao-duc\\thu-khoa-kep-duoc-thang-ham-som-cua-hoc-vien-an-ninh-4529223.txt", "r",encoding="utf-8") as f:
#     a =f.read()
# print(analysis(a))