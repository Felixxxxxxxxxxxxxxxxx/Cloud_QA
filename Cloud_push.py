## run in the Cloud
import pymysql
import random
import json
import requests
import datetime,time

class wx_push(object):

    CID = "wwf374186257aa440e"
    AID = "1000003"
    SECRET = "-We5QhnTDMRvPfM0oJKqIfqZQL0lpOalhAKIwv5hAT8"
    sendkey="061218Cancer*"

    def push_decision(via):

        if via=='rwth':
            wx_push.AID = "1000003"
            wx_push.SECRET = "-We5QhnTDMRvPfM0oJKqIfqZQL0lpOalhAKIwv5hAT8"
        if via=='important':
            wx_push.AID = "1000002"
            wx_push.SECRET = "2VxW1rBLLFYo31IExa1AGT0sS7H6WUGdKeViJ09-XLs"




    def send_to_wecom(text,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
        get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(wecom_cid,wecom_secret)
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        if access_token and len(access_token) > 0:
            send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
            data = {
                "touser":wecom_touid,
                "agentid":wecom_aid,
                "msgtype":"text",
                "text":{
                    "content":text
                },
                "duplicate_check_interval":600
            }
            response = requests.post(send_msg_url,data=json.dumps(data)).content
            return response
        else:
            return False


    def send_to_wecom_markdown(text,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
        get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(wecom_cid,wecom_secret)
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        if access_token and len(access_token) > 0:
            send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
            data = {
                "touser":wecom_touid,
                "agentid":wecom_aid,
                "msgtype":"markdown",
                "markdown":{
                    "content":text
                },
                "duplicate_check_interval":600
            }
            response = requests.post(send_msg_url,data=json.dumps(data)).content
            return response
        else:
            return False


class Database(object):

    dbhost='localhost'
    dbuser='root'
    dbpassword='061218cancer'

    def pick_random_value(table_name,db_name='cancer'):
        # 打开数据库连接
        db = pymysql.connect(host=Database.dbhost,
                            user=Database.dbuser,
                            password=Database.dbpassword,
                            database=db_name
                            )
        cursor = db.cursor()

        sql =  'SELECT * FROM {}'.format(table_name)

        try:
            cursor.execute(sql)
            get_row = cursor.fetchall()
            db.commit()
            n=len(get_row)
            i= random.randint(0,n)

            if table_name == 'Question':
                return str(str(get_row[i][0])+".\n"+str(get_row[i][1])+"\n"+str(get_row[i][2]))
            if table_name == 'Fixed_collocation':
                return str(str(get_row[i][0])+".\n"+str(get_row[i][1])+"\n"+str(get_row[i][2])+"\n"+str(get_row[i][3]))
            
        except:
            print("Display value error")
            db.rollback()
            
        cursor.close()
        db.close()


def Push(text,via='rwth'):
        wx_push.push_decision(via)
        ret = wx_push.send_to_wecom(text, wx_push.CID, wx_push.AID , wx_push.SECRET)
        return(ret)

hour = 30
while True:    
    now_time = datetime.datetime.now()
    if now_time.hour != hour & now_time.hour > 10:
        QA = Database.pick_random_value(table_name="Question")
        Push(QA)
        FC = Database.pick_random_value(table_name="Fixed_collocation")
        Push(FC)
        hour = now_time.hour
        time.sleep(50*60)  

