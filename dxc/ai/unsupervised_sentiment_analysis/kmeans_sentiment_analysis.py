# import re
# import nltk
# import spacy
# import gensim
# import numpy as np
# import unicodedata
# import pandas as pd
# nltk.download('punkt')
# nltk.download('stopwords')
# from bs4 import BeautifulSoup
# from nltk.corpus import stopwords
# from gensim.models import Word2Vec
# from sklearn.cluster import KMeans
# from nltk.tokenize import word_tokenize
# from sklearn.feature_extraction.text import TfidfVectorizer

# def remove_stop_words(data):
#     words = word_tokenize(str(data))
#     new_text = ""
#     for w in words:
#         if w not in stopwords.words('english'):
#             new_text = new_text + " " + w
#     return new_text

# def remove_emails(x):
#     return re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", x)

# def remove_urls(x):
#     return re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '' , x)

# def remove_html_tags(x):
#     return BeautifulSoup(x, 'lxml').get_text().strip()

# def remove_rt(x):
#     return re.sub(r'\brt\b', '', x).strip()

# def remove_accented_chars(x):
#     x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')
#     return x

# def remove_special_chars(x):
#     x = re.sub(r'[^\w ]+', "", x)
#     x = ' '.join(x.split())
#     return x

# def get_text_clean(x):
#     x = str(x).lower().replace('\\', '').replace('_', ' ')
#     x = remove_emails(x)
#     x = remove_urls(x)
#     x = remove_html_tags(x)
#     x = remove_rt(x)
#     x = remove_accented_chars(x)
#     x = remove_special_chars(x)
#     x = re.sub("(.)\\1{2,}", "\\1", x)
#     x = remove_stop_words(x)
#     return x

# def kmeans_sentiment_analyzer(df_TB):
    
#     #tokenize the reviews from dataframe 
#     all_words = [nltk.word_tokenize(sent) for sent in df_TB[df_TB.columns[0]]]
    
#     #generate vectors for tokenized words
#     word2vec = Word2Vec(all_words, min_count=2)
#     vocabulary = word2vec.wv.vocab
    
#     #User will be allowed to pass parameters in further enhancement
#     model = KMeans(n_clusters=2, max_iter=1000, random_state=True, n_init=50).fit(X=word2vec.wv.vectors.astype('double'))
    
#     #Logic need to be enhanced further to generalize the cluster indication
#     positive_cluster_index = 0
    
#     words = pd.DataFrame(word2vec.wv.vocab.keys())
#     words.columns = ['words']
#     words['vectors'] = words.words.apply(lambda x: word2vec[f'{x}'])
#     words['cluster'] = words.vectors.apply(lambda x: model.predict([np.array(x)]))
#     words.cluster = words.cluster.apply(lambda x: x[0])
    
#     words['cluster_value'] = [1 if i==positive_cluster_index else -1 for i in words.cluster]
#     words['closeness_score'] = words.apply(lambda x: 1/(model.transform([x.vectors]).min()), axis=1)
#     words['sentiment_coeff'] = words.closeness_score * words.cluster_value
    
#     words[['words', 'sentiment_coeff']].to_csv('sentiment_dictionary.csv', index=False)
    
#     print('words processed and coefficients stored in sentiment_dictionary.csv')
    
    

# def create_tfidf_dictionary(x, transformed_file, features):
#     vector_coo = transformed_file[x.name].tocoo()
#     vector_coo.col = features.iloc[vector_coo.col].values
#     dict_from_coo = dict(zip(vector_coo.col, vector_coo.data))
#     return dict_from_coo

# def replace_tfidf_words(x, transformed_file, features):
#     dictionary = create_tfidf_dictionary(x, transformed_file, features)   
#     return list(map(lambda y:dictionary[f'{y}'], x.Reviews.split()))

# def replace_sentiment_words(word, sentiment_dict):
#     try:
#         out = sentiment_dict[word]
#     except KeyError:
#         out = 0
#     return out
    
# def kmeans_sentiment_predictor(df_predict):
#     sentiment_map = pd.read_csv('sentiment_dictionary.csv')
#     sentiment_dict = dict(zip(sentiment_map.words.values, sentiment_map.sentiment_coeff.values))
#     file_weighting = df_predict.copy()
#     file_weighting.columns = ['Reviews', 'Sentiment']
    
#     tfidf = TfidfVectorizer(tokenizer=lambda y: y.split(), norm=None)
#     tfidf.fit(file_weighting.Reviews)
#     features = pd.Series(tfidf.get_feature_names())
#     transformed = tfidf.transform(file_weighting.Reviews)
    
#     replaced_tfidf_scores = file_weighting.apply(lambda x: replace_tfidf_words(x, transformed, features), axis=1)
    
#     replaced_closeness_scores = file_weighting.Reviews.apply(lambda x: list(map(lambda y: replace_sentiment_words(y,
#                                 sentiment_dict), x.split())))
    
    
#     new_df = pd.DataFrame(data=[replaced_closeness_scores, replaced_tfidf_scores,
#                                         file_weighting.Reviews,file_weighting.Sentiment]).T
#     new_df.columns = ['sentiment_coeff', 'tfidf_scores', 'sentence', 'sentiment']
#     new_df['sentiment_rate'] = new_df.apply(lambda x: np.array(x.loc['sentiment_coeff']) @
#                                                             np.array(x.loc['tfidf_scores']), axis=1)
#     new_df['prediction'] = (new_df.sentiment_rate>0).astype('int8')
#     new_df['sentiment'] = [1 if i==1 else 0 for i in new_df.sentiment]
    
#     return new_df[['sentence','prediction']]
