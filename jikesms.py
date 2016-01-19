# encoding:utf-8

import sys, requests, time, random, json, hashlib

reload(sys)
sys.setdefaultencoding('utf8')


class JikeSms(object):
    def __init__(self):
        self.base_url = 'http://www.jikesms.com/common/ajax.htm'
        self.pid = '58'
        self.user_uid = 'wfight'
        self.user_pwd = '12345zxcvb'
        data = {
            'action': 'user:UserEventAction',
            'event_name_login': u'提交',
            'uid': 'wfight',
            'password': hashlib.md5('12345zxcvb').hexdigest(),
            'useToken': 'true'
        }
        resp_json = requests.post(self.base_url, data=data).json()
        if resp_json['succeed']:
            print u'余额:', resp_json['model']['money']
            self.token = resp_json['model']['token']
            pass
        else:
            print u'登录失败', resp_json['model']['message']

    pass


    def get_mobile_num(self):
        data = {
            'action': 'phone:PhoneEventAction',
            'event_name_getPhone': u'提交',
            'serviceId': '58',
            'token': self.token
        }
        while True:
            try:
                # 获得的直接是mobile num
                resp_json = requests.post(self.base_url, data=data).json()
            except:
                continue
            if resp_json['succeed']:
                mobile_num= resp_json['model']['phone']
                print u'获得手机号码:',mobile_num
                return mobile_num
            else:
                print u'获取号码失败', resp_json['model']['message']
            pass
        pass


    def get_code_and_release_mobile(self, mobile_num):
        data = {
            'action': 'phone:PhoneEventAction',
            'event_name_getMessage': u'提交',
            'partnerId': 'wfight',
            'serviceId': '58',
            'phone': mobile_num,
            'token': self.token
        }
        cnt = 0
        while cnt < 20:
            cnt += 1
            try:
                resp_json = requests.post(self.base_url, data=data,timeout=10).json()
            except:
                print u'获取验证码异常'
                time.sleep(3)
                continue
            if resp_json['succeed']:
                sms_msg = resp_json['model']['message']
                print u'短信内容:', sms_msg
                end = sms_msg.find('，')
                start = end - 6
                return sms_msg[start:end]
                pass
            else:
                err_msg= resp_json['model']['message']
                print u'获取验证码失败:',err_msg
                # 该手机已释放或已加入黑名单！
                if u'释放' in err_msg:
                    return None
            time.sleep(3)
        return None
        pass


    def add_ingore_list(self, mobile_nums):
        data = {
            'action': 'phone:PhoneEventAction',
            'event_name_addBlacklist': u'提交',
            'serviceId': '58',
            'phone': mobile_nums,
            'token': self.token
        }
        try:
            resp_json = requests.post(self.base_url, data=data).json()
        except:
            print mobile_nums,u'添加黑名单失败，请手动加黑'
            return
        if resp_json['succeed']:
            print mobile_nums, u'添加黑名单成功'
            pass
        else:
            print u'添加黑名单失败', resp_json['model']['message']

        pass


if __name__ == '__main__':
    # y = YunMa()
    # mobile_num = y.get_mobile_num()
    # print mobile_num
    # mobile_num='13927295915,13081364149'
    # y.add_ingore_list(mobile_num)
    #y.get_recving_info()
    # a="""[{"Recnum":"15778045394","Pid":["65"],"Timeout":"2015-05-04 20:24:40","Start_time":"2015-05-04 20:21:40"}]"""
    # b=json.loads(a)
    # print b
    # print [j['Recnum'] for j in b]
    #print hashlib.md5('765081406').digest()
    js = JikeSms()
    print js.get_mobile_num()
    pass
