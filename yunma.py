# encoding:utf-8

import sys, requests, time, random, json, hashlib

reload(sys)
sys.setdefaultencoding('utf8')


class YunMa(object):
    def __init__(self):
        self.base_url = 'http://api.vim6.com/DevApi/'
        self.pid = '65'
        self.user_uid = 'wfight'
        self.user_pwd = '12345zxcvb'
        self.uid = '48683'
        # login_url = self.base_url + ('loginIn?uid=%s&pwd=%s' % (self.user_uid, self.user_pwd))
        login_url = 'http://api.vim6.com/DevApi/loginIn?uid=wfight&pwd=12345zxcvb'
        resp_json = requests.get(login_url, timeout=5).json()
        # print resp_json
        # self.uid = resp_json['Uid']
        self.token = resp_json['Token']

    pass

    def get_mobile_num(self):
        # url = self.base_url + ('getMobilenum?uid=%s&token=%s&pid=%s' % (self.uid, self.token, self.pid))
        url = 'http://api.vim6.com/DevApi/getMobilenum?uid=40503&pid=65&token=%s' % self.token
        # 获得的直接是mobile num
        try_cnt = 0
        while try_cnt < 15:
            try_cnt += 1
            try:
                mobile_num = requests.get(url, timeout=10).text
            except:
                print u'尝试获取手机号次数:', try_cnt
                continue
            if mobile_num == 'No_Data':
                print u'服务器暂时没有手机号，循环获取'
                try_cnt -= 1
                continue
            print u'获得手机号码:', mobile_num

            return mobile_num
            pass
        return None
        pass

    def get_code_and_release_mobile(self, mobile_num):
        # url = self.base_url + ('getVcodeAndReleaseMobile?uid=%s&token=%s&mobile=%s&author_uid=%s&pid=%s' % (self.uid, self.token, mobile_num, self.user_uid, self.pid))
        url = 'http://api.vim6.com/DevApi/getVcodeAndReleaseMobile?uid=40503&token=%s&mobile=%s&author_uid=jiuyueguang&pid=65' % (
            self.token, mobile_num)
        cnt = 0
        while cnt < 19:
            cnt += 1
            try:
                text = requests.get(url, timeout=10).text
            except:
                print cnt, u'获取验证码异常'
                time.sleep(3)
                continue
            print cnt, text
            if text.find(mobile_num) != -1:  # 成功返回了
                end = text.find('，')
                start = end - 6
                return text[start:end]
            time.sleep(5)
        return None
        pass

    def add_ingore_list(self, mobile_nums):
        # url = self.base_url + ('addIgnoreList?uid=%s&token=%s&pid=%s&mobiles=%s' % (self.uid, self.token, self.pid, mobile_nums))
        url = 'http://api.vim6.com/DevApi/addIgnoreList?uid=40503&token=%s&pid=65&mobiles=%s' % (
            self.token, mobile_nums)
        try:
            requests.get(url, timeout=10)
        except:
            print mobile_nums, u'添加黑名单失败，请手动加黑'
            return
        print mobile_nums, u'添加到黑名单'
        pass

    def get_recving_info(self):
        # url = self.base_url + ('getRecvingInfo?uid=%s&token=%s&pid=%s' % (self.uid, self.token, self.pid))
        url = 'http://api.vim6.com/DevApi/getRecvingInfo?uid=40503&token=%s&pid=65' % self.token
        try:
            resp_json = requests.get(url).json()
        except:
            return
        resp_json = json.loads(resp_json)
        all_numbers = [j['Recnum'] for j in resp_json]
        if len(all_numbers) == 0:
            return
        all_numbers = ','.join(all_numbers)
        print 'all received nums:', all_numbers
        self.add_ingore_list(all_numbers)
        pass

    def cancel_sms_recv(self, mobile_num):
        # 取消一个短信接收，可立即解锁被锁定的金额
        url = 'http://api.vim6.com/DevApi/cancelSMSRecv?uid=40503&token=%s&mobile=%s' % (self.token, mobile_num)
        try:
            requests.get(url, timeout=10)
        except:
            print mobile_num, u'取消短信接收失败'
            return
        print mobile_num, u'取消短信接收成功:)'
        pass


if __name__ == '__main__':
    y = YunMa()
    # mobile_num = y.get_mobile_num()
    # print mobile_num
    # mobile_num='13927295915,13081364149'
    # y.add_ingore_list(mobile_num)
    y.get_recving_info()
    # a="""[{"Recnum":"15778045394","Pid":["65"],"Timeout":"2015-05-04 20:24:40","Start_time":"2015-05-04 20:21:40"}]"""
    # b=json.loads(a)
    # print b
    # print [j['Recnum'] for j in b]
    pass
