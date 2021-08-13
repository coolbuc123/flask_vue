from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import derivative as drv

import os
import pandas as pd
from datetime import datetime
import json

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
CORS(app)

date_list = ''

def py_logic(post_data):
    data_dic, dates_dic = '', ''
    
    con = drv.db_connect()
    
    # 기준일 여부 확인
    selected_date = post_data['selected']
    received = post_data['received']
    print(f"←------From Vue : {selected_date}, 받은적 있지? {received}")
    
    # 날짜 List 읽어오기
    dates = drv.get_date_list(con)
#     dates['date'] = pd.to_datetime(dates['date']).dt.strftime('%Y-%m-%d')
    
    # 기준일이 없는 최초 POST 시 DB의 날짜List를 1회 가져오고 최근일을 기준일로 세팅
    if selected_date == '0000-00-00':
        selected_date = dates['date'].iloc[0]
#         selected_date = datetime.today().strftime('%Y-%m-%d') # 당일을 기준일로
        #         print(f"dates.iloc[0]확인 : {dates['date'].iloc[0]}")
    dates_dic = dates.to_dict()

    print(f"{selected_date} 수익률 조회하겠습니다.")
    msg, data = drv.get_drv_result(con, selected_date)
    data = data.round(2)
    
    print('수신받은 msg 확인:', msg)
    if msg == '성공':
        for col_name, col_data in data.iteritems():
            data[col_name] = col_data.astype('str').str.zfill(3)

        print(data)
        data_dic = data.to_dict() 
        
        total = {
            'msg':msg,
            'date':dates_dic, 
            'data':data_dic, 
            'sel_date':selected_date
        }
    
    else:
        total = {
            
            
            'msg':msg,
            'date':dates_dic, 
            'data':['0000-00-00'], 
            'sel_date':selected_date 
        }
        
    rt = json.dumps(total) # dic → json (참고)json → dic >>> json.loads(js)                
    return rt


@app.route("/test", methods=['GET', 'POST', 'PUT', 'DELETE'])
def test():
    if request.method == 'POST':
        print('POST')
        
        # Python logic Action 
        post_data = request.get_json()
        result_json = py_logic(post_data)
        
        print("--------------------------------------------------------------------------")
        print("dic : ", result_json)
        print("--------------------------------------------------------------------------")        

        return make_response(result_json, 200)

    if request.method == 'GET':
        print('GET')
        user = request.args.get('email')
        print(user)
        
    if request.method == 'PUT':
        print('PUT')
        user = request.args.get('email')
        print(user)
        
    if request.method == 'DELETE':
        print('DELETE')
        user = request.args.get('email')
        print(user)

    return make_response(jsonify({'status': request.method }), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8082")

