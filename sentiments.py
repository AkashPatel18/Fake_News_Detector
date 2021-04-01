from textblob import TextBlob
from newspaper import Article


def calsentiment(input):
    article = Article(input,language = 'en')
    article.download()
    article.parse()
    article.nlp()
    article_text = article.text
    text = TextBlob(article_text)
    senti = text.sentiment

    return senti