# DANeS

## 1. Giới thiệu

DANeS viết tắt của "DATASET.VN and [AIV-Group](https://aivgroup.vn) News Sentiment". Đây là 1 dự án mã nguồn mở giúp phân loại chủ đề và sắc thái của các tiêu đề bài viết với sự hợp tác của DATASET JSC (dataset.vn) và AIV Group (aivgroup.vn).

Tài liệu này hướng dẫn cách training mô hình phân loại chủ đề và sắc thái bằng Fasttext. FastText là thư viện mã nguồn mở do Facebook tạo ra năm 2016, nó hỗ trợ việc huấn luyện phép nhúng từ và phân loại văn bản.

## 2. Cài đặt

Cài đặt các gói cần thiết:

* fasttext
* underthesea

## 3. Training model

### 3.1 Import các thư viện cần thiết

```python
import pandas as pd
import numpy as np
import regex as re
import fasttext
from underthesea import word_tokenize
from sklearn.model_selection import train_test_split
```

### 3.2 Viết các hàm xử lý dữ liệu text

* Tách từ (từ đơn, từ ghép), chuyển các từ về chữ viết thường, loại bỏ các khoảng trắng liên tiếp

```python
def text_preprocess(document):
    document = word_tokenize(document, format="text")
    document = document.lower()
    document = re.sub(r'\s+', ' ', document).strip()
    return document
```

* Loại bỏ các stopword: Phần này chúng tôi dùng danh sách stopword tự tạo ra, có thể thay thế bằng các tài liệu bất kỳ.

```python
data = pd.read_csv('./stopwords.csv', encoding='utf-8')
list_stopwords = data['stopwords'].tolist()

def remove_stopwords(document):
    words = []
    for word in document.strip().split():
        if word not in list_stopwords:
            words.append(word)
    return ' '.join(words)
```

### 3.3 Nhập dữ liệu các tiêu đề bài báo và xử lý

* Dữ liệu nhập vào dạng

```python
df = pd.read_csv('500ksample.csv', encoding="utf-8")
df.head()
```

title|publish_date|topic|sentiment
--------------|--------------|--------------|--------------
Vaccine COVID-19 dạng xịt mũi được thử nghiệm ...	| 2021-10-13 13:52:31+00:00| chinh_tri| 1
Mưa lũ làm 8 người thương vong và mất tích, gâ...	| 2021-10-17 23:16:28+00:00| moi_truong| 2

Trong đó:

`title` là tiêu đề bài viết

`publish_date` là thời điểm bài viết được xuất bản

`topic` là chủ đề của bài viết: Chính trị, Môi trường, Đời sống, Thời sự,...

`sentiment` là sắc thái bài viết: 1: Tích cực, 2: Tiêu cực, 3: Trung tính.

* Xử lý dữ liệu, chuyển về dạng phù hợp với gói fasttext

```python
df['sentiment'] = df['sentiment'].astype(str)
df.loc[:, 'sentiment'] = df.loc[:, 'sentiment'].apply(lambda x: '__label__' + x)
df.loc[:, 'topic'] = df.loc[:, 'topic'].apply(lambda x: '__label__' + x)
df = df[['title', 'topic', 'sentiment']]

df['title'] = df['title'].apply(text_preprocess)
df['title'] = df['title'].apply(remove_stopwords)
```

* Chia tập train, test  với tỷ lệ 8/2

```python
train, test = train_test_split(df, test_size = 0.2, random_state=42)
```

* Lưu lại tập train, test để sử dụng fasttext

```python
# Data topic model:
train[['topic', 'title']].to_csv('train1.txt', index = False, sep = ' ', header = None)
test[['topic', 'title']].to_csv('test1.txt', index = False,  sep = ' ', header = None)
# Data sentiment model:
train[['sentiment', 'title']].to_csv('train2.txt', index = False, sep = ' ', header = None)
test[['sentiment', 'title']].to_csv('test2.txt', index = False,  sep = ' ', header = None)
```

### 3.4 Train model, đánh giá với tập test, lưu lại model

* Chủ đề

```python
# Training the fastText classifier topic
model1 = fasttext.train_supervised('train1.txt', dim=100, epoch=5, lr=0.1, wordNgrams=5, label='__label__')
# Evaluating performance on the entire test file
model1.test('test1.txt')   
model1.save_model('model1.bin')
```

* Sắc thái

```python
# Training the fastText classifier sentiment
model2 = fasttext.train_supervised('train2.txt', dim=100, epoch=5, lr=0.1, wordNgrams=5, label='__label__')
# Evaluating performance on the entire test file
model2.test('test2.txt')   
model2.save_model('model2.bin')
```

### 3.5 Load model, áp dụng với dữ liệu mới

```python
model1 = fasttext.load_model('model1.bin')
model2 = fasttext.load_model('model2.bin')
document = "Trong không khí trang nghiêm, tiếng chuông chùa, nhà thờ ngân vang, người dân khắp cả nước cùng chắp tay cầu nguyện, thắp nến, thả hoa đăng tưởng niệm hơn 23.000 người mất vì Covid-19."

document = text_preprocess(document)
document = remove_stopwords(document)
pre_topic = model1.predict(document)
pre_sen = model2.predict(document)
result = pd.DataFrame({'topic_raw':[pre_topic[0][0]],
                      'topic_prob':[pre_topic[1][0]],
                      'sen_raw':[pre_sen[0][0]],
                      'sen_prob':[pre_sen[1][0]]
                      })
```

## Hoàn thành!
