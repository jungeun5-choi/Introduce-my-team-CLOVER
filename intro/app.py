from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.w4kj2pc.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

# 메인페이지
@app.route('/')
def home():
    return render_template('team.html')

# 장르별
@app.route('/members')
def member():
    name = request.args.get('name')

    if name == '해인':
        return render_template('member.html')
    elif name == '정은':
        return render_template('member.html')
    elif name == '태훈':
        return render_template('member.html')
    elif name == '지상':
        return render_template('member.html')
    elif name == '형수':
        return render_template('member.html')
    



@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogGenre = soup.select_one('#mainContent > div > div.box_basic > div.info_detail > div.detail_cont > div:nth-child(1) > dl:nth-child(2) > dd').text;

    doc = {
        'title':ogtitle,
        'desc':ogdesc,
        'image':ogimage,
        'comment':comment_receive,    
        'star':star_receive,
        'genre':ogGenre
    }

    db.movies.insert_one(doc)
    
    print(url_receive)
    return jsonify({'msg':'저장 완료!'})

@app.route("/members", methods=["GET"])
def member_get():
    all_member = list(db.members.find({},{'_id':False}))
    return jsonify({'result':all_member})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)