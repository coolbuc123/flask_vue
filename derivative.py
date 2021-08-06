#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql as pydb
pydb.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine
import pandas as pd


# In[2]:


def db_connect():
    user = 'ryuiks'
    password = '1q2w3e4r!!'
    db_name = 'db_aiam_analysis'

    engine = create_engine("mysql+mysqldb://" + user + ":" + password
                           + "@10.17.126.105/" + db_name, encoding='utf-8')
    conn = engine.connect()
    
    return engine


# In[3]:


engine = db_connect()


# In[4]:


def get_drv_result(engine, base_date):
    sql = f"""
      select 
            a.str_code, 
            a.activate, 
            cal_profit(a.str_code, '{base_date}', 0) 1d, 
            cal_profit(a.str_code, '{base_date}', 7) 1w,										
            cal_profit(a.str_code, '{base_date}', 14) 2w, 
            cal_profit(a.str_code, '{base_date}', 30) 1m,										
            cal_profit(a.str_code, '{base_date}', 91) 3m, 
            cal_profit(a.str_code, '{base_date}', 182) 6m,										
            cal_profit(a.str_code, '{base_date}', 365) 1y, 
            cal_profit(a.str_code, '{base_date}', 1000) cum,										
            cal_hit(a.str_code, '{base_date}', 1000) hit, 
            cal_vol(a.str_code, '{base_date}', 365) vol				
       from dm_strategys a, 
            select_return b 
      where a.str_code = b.str_code 
        and a.activate > 0 
        and b.date = '{base_date}'
      ;
    """
    df = pd.DataFrame()
    try:
        # 쿼리 수행
        df = pd.read_sql_query(sql=sql, con=engine)
        
        # 데이터 정제
        df['activate'] = df['activate'].map({
            1:'전략개발중',
            2:'모의운용중',
            3:'실운용중',
        })
        df['hit'] = df['hit'] * 100
        msg = '성공'
         
    except Exception as e:
        msg = '수익률을 조회할 수 없습니다.'
#         print(f"e {e}")
    return msg, df


# In[5]:


def get_date_list(engine):
    from datetime import datetime
    base_date = datetime.today().strftime('%Y-%m-%d')

    db_start_date = '2021-08-04'
    sql = f"""
        select distinct date 
          from select_return
         where date >= '{db_start_date}'
         order by date desc;
    """
    #{db_start_date} 
    df = pd.read_sql_query(sql=sql, con=engine)
    return df

get_date_list(engine)


# In[6]:


if __name__ == '__main__':
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    print(f"오늘은 {today}")
#     today = '2021-08-04'

    engine = db_connect()
    msg, df = get_drv_result(engine, today)
    print(today, msg)
    date = get_date_list(engine)
    print(df.shape)
    print(df.head(3))
    print(date)

