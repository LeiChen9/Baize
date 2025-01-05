'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2025-01-05 14:11:57
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2025-01-05 14:34:19
FilePath: /Code/Baize/app.py
Description: 

Copyright (c) 2025 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
from flask import Flask, request, jsonify
from model.fortune_model import get_daily_fortune

app = Flask(__name__)

@app.route('/predict_fortune', methods=['POST'])
def predict_fortune():
    data = request.get_json()
    zodiac = data.get('zodiac')
    mbti = data.get('mbti')
    
    fortune = get_daily_fortune(zodiac, mbti)
    return jsonify({'fortune': fortune})

if __name__ == '__main__':
    app.run(debug=True)