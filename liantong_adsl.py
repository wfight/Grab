# encoding:gbk

import os, requests, sys, time
from liantong_model import Session, MyProxy

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
           "Host": "1111.ip138.com",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "keep-alive"
           }


class Adsl(object):
    # 联通adsl
    def __init__(self):
        self.adsl_name = 'ADSL'
        self.user_name = '030008002565'
        self.user_pwd = 'va123456'
        self.curr_proxy = None
        self.db_s = Session()
        pass

    def connect(self):
        conn_cmd = 'rasdial PPPOE 99392213 123456 1>nul'
        while True:
            try:
                conn_ret = os.system(conn_cmd)
                if conn_ret == 0:
                    break
            except:
                continue  # 一般会出现691的错误，重连 99392213----123456
                pass
        print 'adsl connected'
        pass

    def disconnect(self):
        disconn_cmd = 'rasdial /DISCONNECT 1>nul'
        while True:
            try:
                disconn_ret = os.system(disconn_cmd)
                if disconn_ret == 0:
                    break
            except:
                continue  #
                pass
        print 'adsl disconnected'
        pass

    def get138ip(self):
        try_cnt = 0
        while try_cnt < 2:
            try_cnt += 1
            try:
                resp = requests.get('http://1111.ip138.com/ic.asp', headers=headers, timeout=5)
                resp.encoding = 'gbk'
                html_txt = resp.text
                print html_txt[html_txt.find('<center>') + 8:html_txt.find('</center>')]
                # html_txt = requests.get('http://1111.ip138.com/ic.asp',timeout=5).text
            except:
                print u'ip138超时'
                continue
            ip_start = html_txt.find('[') + 1
            ip_end = html_txt.find(']')
            return html_txt[ip_start:ip_end]
        return None
        pass

    def inc_use_cnt(self):
        self.curr_proxy.use_cnt += 1
        self.db_s.add(self.curr_proxy)
        self.db_s.commit()
        pass

    def reconnect(self):
        while True:
            self.disconnect()  # 断开
            self.connect()  # 重连
            ip = self.get138ip()  # 检测ip重复
            if not ip:
                continue
            tmp_ip = self.db_s.query(MyProxy).filter(MyProxy.proxy == ip).first()  # 使用过1次，暂时考虑使用2次为界限
            if not tmp_ip:
                print 'first use ip:', ip
                insert_p = MyProxy()
                insert_p.proxy = ip
                insert_p.use_cnt = 0
                self.curr_proxy = insert_p
                return insert_p
            elif tmp_ip.use_cnt < 2:
                print 'sencond use ip:', ip
                self.curr_proxy = tmp_ip
                return tmp_ip
            # elif tmp_ip.use_cnt < 3:
            #     print 'third use ip:', ip
            #     self.curr_proxy = tmp_ip
            #     return tmp_ip
            else:
                print 'already use 2 times ip:', ip

        pass

    pass


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    asdl = Adsl()
    i = 0
    while i < 1000:
        i += 1
        print i
        asdl.reconnect()
        pass

    pass
