from flask import Flask, render_template, request
from textblob import TextBlob
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def save_to_db(text, sentiment, score):
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Root@123',  # <-- CHANGE THIS to your MySQL password
        database='intern'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO reviews(text, sentiment, score) VALUES (%s, %s, %s)"
    cursor.execute(sql, (text, sentiment, score))
    conn.commit()
    cursor.close()
    conn.close()

def get_sentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.1:
        return "Positive", round(score, 2)
    elif score < -0.1:
        return "Negative", round(score, 2)
    else:
        return "Neutral", round(score, 2)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_text = request.form['text']
        sentiment, score = get_sentiment(user_text)
        save_to_db(user_text, sentiment, score)
        result = {'text': user_text, 'sentiment': sentiment, 'score': score}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)