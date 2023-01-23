import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from flask import request,Flask,render_template
app=Flask(__name__)
@app.route('/')
def home():
     return render_template('index.html')

@app.route('/' ,methods=['POST'])
def predict():
    text=request.form['text']
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    text=re.sub(emoj, ' ', text)
    text=re.sub(r'http\S+', ' ',text)
    CLEANR = re.compile('<.*?>')
    text = re.sub(CLEANR, ' ', text)
    text=re.sub(r'[0-9]+',' ',text)
    text=re.sub(r'[^\w\s]', ' ', text)
    text=re.sub(r"[\([{})\]]", " ", text)
    text=' '.join([word for word in text.split()])
    analyzer=SentimentIntensityAnalyzer()
    score=analyzer.polarity_scores(text)['compound']
    if score>0:
        label='Sentiment of the entered sentence is Positive'
        return render_template('index.html',positive=label)
    elif score<0:
        label='Sentiment of the entered sentence is Negative'
        return render_template('index.html',negative=label)
if __name__ == '__main__':
    app.run(debug=True)