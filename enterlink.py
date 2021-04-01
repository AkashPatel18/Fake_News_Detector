from newspaper import Article
import re

def articlethroughlink(link):
    article = Article(link,language = 'en')
    article.download() 
    article.parse()
    article.nlp()
    title = article.title
    #print(title)
    articletext = article.text
    #print(articletext)

    articlesource = article.authors
    #print(articlesource)

    try:
        if(len(articlesource)==0):
            text = re.sub(r'https://www.','',link)
            text = re.sub(r'.com\S+','',text)
            text = re.sub(r'https\S','',text)
            authorsource = re.sub(r'//','',text)
        else:
            text = re.sub(r'https://www.','',link)
            text = re.sub(r'.com\S+','',text)
            text = re.sub(r'https\S','',text)
            authorsource = re.sub(r'//','',text)

        
    except TypeError:
        print("TypeError")

    finaltext = title + ' '+ authorsource + ' '+ articletext
    return finaltext



