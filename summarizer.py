from newspaper import Article


def summarize(input):
    article = Article(input,language = 'en')
    article.download()
    article.parse()
    article.nlp()
    summarized_output = article.summary
    return summarized_output


    