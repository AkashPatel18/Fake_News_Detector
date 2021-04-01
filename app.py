import pickle
from flask import Flask, render_template, request
from enterlink import articlethroughlink
import re
import nltk
from nltk.stem import WordNetLemmatizer
from summarizer import summarize
from sentiments import calsentiment
lm = WordNetLemmatizer()
stopword = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
            'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such']

tfidf = pickle.load(open('tfidf.pkl', 'rb'))
model = pickle.load(open('fakenews.pkl', 'rb'))


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        rawtext = request.form['title'] + " " + \
            request.form['author'] + " " + request.form['maintext']

        corpus = []
        news = re.sub('[^a-zA-Z]', ' ', rawtext)
        news = news.lower()
        news = news.split()
        news = [lm.lemmatize(word) for word in news if not word in stopword]
        news = ' '.join(news)
        corpus.append(news)

        vector = tfidf.transform(corpus).toarray()
        print(vector.shape)
        prediction = model.predict(vector)
        print(prediction)
        prob = model.predict_proba(vector)
        print(prob)
        prob = round((prob.max())*100)

    return render_template('index.html', result=prediction, result1=prob)




@app.route('/vialink', methods=['POST'])
def vialink():
    if request.method == "POST":

        textvialink = request.form['Link']
        rawtext = articlethroughlink(textvialink)
        
        corpus = []
        news = re.sub('[^a-zA-Z]', ' ', rawtext)
        news = news.lower()
        news = news.split()
        news = [lm.lemmatize(word) for word in news if not word in stopword]
        news = ' '.join(news)
        corpus.append(news)
        vectors = tfidf.transform(corpus).toarray()
        predictions = model.predict(vectors)
        probs = model.predict_proba(vectors)
        prob = round((probs.max())*100)
        inputtext = textvialink
        summerized_text = summarize(inputtext)
        senti = calsentiment(inputtext)
        sentiment = senti[0]
        sentiment1 = senti[1]

        if sentiment > 0.75:
            sentiment_category = "Extremely positive."
        elif sentiment > 0.5:
            sentiment_category = "Significantly positive."
        elif sentiment > 0.3:
            sentiment_category = "Fairly positive."
        elif sentiment > 0.1:
            sentiment_category = "Slightly positive."
        elif sentiment < -0.1:
            sentiment_category = "Slightly negative."
        elif sentiment < -0.3:
            sentiment_category = "Fairly negative."
        elif sentiment < -0.5:
            sentiment_category = "Significantly negative."
        elif sentiment < -0.75:
            sentiment_category = "Extremely negative."
        else:
            sentiment_category = "Neutral."

        if sentiment1 > 0.75:
            sentiment_category1 = "Extremely subjective."
        elif sentiment1 > 0.5:
            sentiment_category1 = "Fairly subjective."
        elif sentiment1 > 0.3:
            sentiment_category1 = "Fairly objective."
        elif sentiment1 > 0.1:
            sentiment_category1 = "Extremely objective."

    return render_template('index.html', result=predictions, result1=prob, summerized_text=summerized_text, polarity=sentiment_category, subjectivity=sentiment_category1)




if __name__ == "__main__":
    app.run(debug=True)
