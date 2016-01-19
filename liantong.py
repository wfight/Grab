# encoding:gbk

import requests, time, random, sys, traceback, os, socket, re
import win32api, win32pdhutil, win32con
from selenium.webdriver.common.keys import Keys
import win32com.client
from bs4 import BeautifulSoup
from win32com.client import Dispatch
from datetime import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from liantong_model import *
from sqlalchemy.sql.expression import func
from yunma import *
from jikesms import *
from liantong_adsl import Adsl
from settings import *

reload(sys)
sys.setdefaultencoding('utf8')

# pingjia_xpath = 'html/body/div[1]/table[%s]/tbody/tr[2]/td[10]/a'
# rc = re.compile(ur'��')
autoit = Dispatch("AutoItX3.Control")
driver = None
img_path_driver = 'C:\\'


def set_driver():
    # first kill browser process
    os.system('taskkill /f /im chrome.exe')
    os.system('taskkill /f /im chromedriver.exe')
    global driver
    co = webdriver.ChromeOptions()
    ua = '--user-agent=' + random.choice(mobile_user_agents)
    co.add_argument(ua)
    prefs = {"profile.default_content_settings.geolocation": 2}
    co.add_experimental_option("prefs", prefs)
    co.add_argument("--incognito")  # ����ģʽ��Ҫ����cookies�Ƿ����������
    driver = webdriver.Chrome(chrome_options=co)
    driver.delete_all_cookies()
    driver.set_page_load_timeout(60)
    pass


def get_pgtid():
    return str(int(time.time() - random.randint(10, 100))) + str(random.randint(1000, 9999)) + '.' + str(
        random.randint(1000000000000000, 9999999999999999))
    pass


def get_element(d, by_type, value):
    # print value
    try:
        element = WebDriverWait(d, 30).until(EC.presence_of_element_located((by_types[by_type], value)))
    except:
        return None
    # return driver.find_element(by_types[by_type], value)
    return element
    pass


def get_datehour():
    dtn = datetime.now()
    today_date = dtn.day
    day_offset = days_per_month[dtn.month - 1] - today_date
    if day_offset > 2:  # �����ǽ��죬���죬���죬Ҫ���ǵ���ĩ
        day_offset = 2
    choice_date = today_date + random.randint(0, day_offset)
    hour_str = str(random.randint(10, 19))
    if choice_date == today_date:  # ����ǽ��죬ʱ��Ӧ�ô��ڵ�ǰʱ��
        if 19 - dtn.hour < 1:
            choice_date += 1
        else:
            hour_int = dtn.hour + random.randint(1, 19 - dtn.hour)
            hour_str = str(hour_int) if hour_int > 9 else ('0' + str(hour_int))
        pass
    date_str = dtn.strftime('%Y-%m-') + (str(choice_date) if choice_date > 9 else ('0' + str(choice_date)))
    return (date_str, hour_str)
    pass


def get_user_name_from_cookies(driver, cookie_name, find_str):
    tmp_cookie = driver.get_cookie(cookie_name)
    if tmp_cookie:
        tmp_cookie_value = tmp_cookie['value']
        if tmp_cookie_value:
            find_str_start = tmp_cookie_value.find(find_str) + len(find_str)
            find_str_end = tmp_cookie_value.find('&', find_str_start)
            user_name = tmp_cookie_value[find_str_start:find_str_end]
            if user_name:
                return user_name
            pass
        pass
    return ''
    pass


def write_no_succ_into_file(mobile_num, vcode):
    print u'��¼û�гɹ����ֻ��ź���֤��'
    with open('no_succ.txt', 'a') as f:
        f.write(mobile_num + '|' + vcode + '\n')
    pass


def get_user_name(driver):
    # �ֻ���ҳ�˴�cookies�л��username
    # �ȴ�58cooper�л�ã������www58comȡ�ã������PPU��ȡ��
    return get_user_name_from_cookies(driver, '58cooper', 'username=') or \
           get_user_name_from_cookies(driver, 'www58com', 'UserName=') or \
           get_user_name_from_cookies(driver, 'PPU', 'UN=')
    pass


def vcode_from_web(driver):
    flag = 1
    get_mobile_try_cnt = 0
    while get_mobile_try_cnt < 2:
        mobile_num = global_y.get_mobile_num()  # ��ȡ�ֻ���
        if not mobile_num:
            global_adsl.reconnect()
            continue
        driver.execute_script("document.getElementById('phone').value='" + mobile_num + "';")
        time.sleep(1)
        driver.execute_script("document.getElementById('code_sender').click();")
        time.sleep(10)
        try:
            driver.switch_to_alert().accept()
            print u'alert �����ˣ�����'
            global_y.cancel_sms_recv(mobile_num)  # ȡ�����Ž���
            driver.switch_to_default_content()
            return (None, None)
        except:
            print u'û��alert'
            pass
        # driver.execute_script("document.getElementById('phone').value='" + mobile_num + "';")
        # time.sleep(1)
        # driver.execute_script("document.getElementById('code_sender').click();")
        # time.sleep(10)
        code_num = global_y.get_code_and_release_mobile(mobile_num)
        # ע���жϣ����codeΪNone����Ҫ���˺���Ӻڲ����»�ȡ�������֤��
        if code_num:
            driver.execute_script("document.getElementById('valicode').value='" + code_num + "';")
            # time.sleep(1)
            # driver.execute_script("document.getElementById('orderbutton').className+=' btn-gray';");
            # driver.execute_script("document.getElementById('code_sender').className='btn-yzm btn-gray disabled';");
            break
        else:
            global_y.add_ingore_list(mobile_num)
        get_mobile_try_cnt += 1
    if get_mobile_try_cnt >= 2:  # ����
        print u'��ȡ�ֻ��Ŵ���̫�࣬����������'
        return (None, None)
    return (mobile_num, code_num)
    pass


def vcode_from_file(driver):
    with open('no_succ.txt', 'r') as f:
        mobile_num_vcode_list = f.readlines()
    if len(mobile_num_vcode_list) == 0:
        print u'�ļ���û����'
        return (None, None)
    mobile_num_vcode = mobile_num_vcode_list[0]
    mobile_num_vcode_list = mobile_num_vcode_list[1:]
    with open('no_succ.txt', 'w+') as f:
        f.writelines(mobile_num_vcode_list)
    mobile_num = mobile_num_vcode[0:11]
    code_num = mobile_num_vcode[12:18]
    print u'��Դ���ļ�', mobile_num, code_num
    driver.execute_script("document.getElementById('phone').value='" + mobile_num + "';")
    driver.execute_script("document.getElementById('valicode').value='" + code_num + "';")
    return (mobile_num, code_num)
    pass


def get_vcode(driver):
    is_from_web_api = False
    mobile_num, code_num = vcode_from_file(driver)
    if not mobile_num:
        # �ļ���û���ˣ���web�ӿڻ�ȡ
        mobile_num, code_num = vcode_from_web(driver)
        is_from_web_api = True
        pass
    return (is_from_web_api, mobile_num, code_num)
    pass


def m_yuyue(s, user, href):
    try:
        driver.execute_script('window.stop();')  # ����ͣ����
        driver.delete_all_cookies()  # ��ɾ��
    except:
        set_driver()
    try:
        erji_domain_end = href.find('.')
        com_domain_end = href.find('/', erji_domain_end)
        erji_domain = href[7:erji_domain_end]
        url = 'http://m.58.com/' + erji_domain + href[com_domain_end:]
        try:
            driver.get(url)
            time.sleep(2)
            # driver.refresh()
            # time.sleep(2)
        except:
            print u'��ʱ�쳣'
            driver.execute_script('window.stop();')
            pass
        # print u'��ҳ��ʾԤԼ����:',get_element(driver,'xpath','html/body/div/div[3]/div[2]/a/text()').text
        # print u'��ҳ��ʾ��������:',get_element(driver,'xpath','html/body/div/div[3]/div[2]/a/span[1]').text
        print u'ԭ�����ۺ�ԤԼ:'
        print u'����:', user.original_pingjia_cnt
        print u'ԤԼ:', user.original_yuyue_cnt
        print
        print u'�ͻ�Ҫ�����ۺ�ԤԼ:'
        print u'����:', user.req_pingjia_cnt
        print u'ԤԼ:', user.req_yuyue_cnt
        print
        print u'��ҳǰ̨��ʾ���ۺ�ԤԼ����:'
        try:
            print get_element(driver, 'class', 'commettop_area').text
        except:
            print u'����ԭ��ԤԼ�����۶���0'
        print
        print u'ԭ���ļ������ڵģ�'
        print u'����:', user.pingjia_cnt + user.original_pingjia_cnt
        print u'ԤԼ:', user.yuyue_cnt + user.original_yuyue_cnt
        print
        try:
            yy_url = driver.find_element_by_class_name('btn-djyy').get_attribute('href')
            #driver.execute_script("document.getElementsByClassName('btn-djyy')[0].click();")
        except:
            # pageû�м����ֱ꣬�ӻ�ȡԴ�룬�õ����ӣ�Ȼ��driver.get
            print u'���ԤԼ��ť�쳣��ֱ�ӻ�ȡurl'
            driver.delete_all_cookies()
            HEADER['Host'] = 'm.58.com'
            HEADER['User-Agent'] = random.choice(mobile_user_agents)
            resp = requests.get(url, headers=HEADER, timeout=10)
            if u'��֤��' in resp.text:
                print u'��֤�룡��������������������������������������������'
            yy_url = BeautifulSoup(resp.text, 'html.parser').find('a', class_='btn-djyy').get('href')

            # driver.get(yy_url)
            # time.sleep(2)
            # print u'ԭurl��', yy_url
        yy_url = yy_url.replace('/m2post/', '/mpost/')
        yy_url = yy_url[:yy_url.find('PPGTID')] + 'os=android'

        #print yy_url change to the app link.
        driver.get(yy_url)
        time.sleep(5)
        (date_str, hour_str) = get_datehour()  # ��ȡ���ں�Сʱ
        hour_str += ':00'
        service_time = date_str + ' ' + hour_str
        xingming = random.choice(xing) + random.choice(ming)
        driver.execute_script("document.getElementById('contacts').value='" + xingming + "';")
        driver.execute_script("document.getElementById('selectdate').value='" + service_time + "';")
        # mobile_num, code_num = vcode_from_web(driver)
        is_from_web_api, mobile_num, code_num = get_vcode(driver)
        if not mobile_num:
            return
        driver.execute_script("document.getElementById('code_sender').className='btn-yzm btn-gray disabled';");
        time.sleep(1)
        driver.execute_script("document.getElementById('orderbutton').className+=' flag';");
        time.sleep(1)
        driver.execute_script("document.getElementById('orderbutton').click();")
        time.sleep(5)
        succ_flag = False
        try:
            if get_element(driver, 'class', 'dj_tip1').text.strip()==u'��ϲ���ɹ��Ǽǣ�':
                succ_flag = True
        except:
            pass
        if succ_flag:
            user.yuyue_cnt += 1  # ԤԼ����1
            user.yuyue_per_day_cnt += 1
            user.last_yuyue_time = time.time() + random.randint(444, 666)
            if not user.shop_id:
                # ����shop id
                a = driver.current_url
                shop_id_start = a.find('shopid=') + 7
                shop_id_end = a.find('&', shop_id_start)
                user.shop_id = a[shop_id_start:shop_id_end]
            s.add(user)
            # s.flush()
            p = PingJia()
            # p.user_name = get_element(driver, 'xpath', ".//*[@id='login']/span[1]").text
            p.user_name = get_user_name(driver)
            # print u'ԤԼ�û���', p.user_name
            p.phone = mobile_num
            p.yuyue_time = time.time()
            p.user = user
            p.cookies = str(driver.get_cookies())  # ��¼����ԤԼ��cookies��Ŀ���ǵ�¼��̨ͨ�����׼�¼���¿ͻ�
            s.add(p)
            s.commit()
            #global_adsl.inc_use_cnt()  # ����ip
            print mobile_num, u'ԤԼ�ɹ�:):):):):):):):):):):):):):):):):):):):):)'
        else:
            if is_from_web_api:
                write_no_succ_into_file(mobile_num, code_num)
            print u'û���ҵ���֤XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    except:
        print traceback.print_exc()
        pass
    pass


def do_pingjia(s, pj):
    try:
        driver.execute_script('window.stop();')  # ����ͣ����
        driver.delete_all_cookies()  # ��ɾ��
    except:
        set_driver()
    try:
        pju = pj.user
        ckies = pj.cookies
        if not ckies:
            print u'�� cookies ��Ϣ'
            pj.flag = False
            s.add(pj)
            s.commit()
            return
            # http://m.58.com/bj/?reform=pcfront
        domain_url = 'http://m.58.com/'
        driver.get(domain_url)
        time.sleep(1)
        ckies = eval(ckies)
        if len(ckies) == 0:
            return
        for ck in ckies:
            driver.add_cookie(ck)
        # time.sleep(5)
        order_url = order_base_url % str(int(time.time())) + str(random.randint(100, 999))
        driver.get(order_url)
        time.sleep(3)
        # ����������ַhttp://passport.58.com/login?path=http%3A%2F%2Fmy.58.com%2Fpro%2Fbuyordermgr��˵��cookies���ڻ���ʧЧ�ˣ���־λ����Ϊfalse
        if 'login' in driver.current_url:
            print u'cookies ʧЧ�ˣ����ñ�־λ������'
            pj.flag = False
            s.add(pj)
            s.commit()
            return
        # driver.switch_to_frame('ContainerFrame')
        html_source = driver.page_source  # �õ�iframe�е�Դ��
        parse_order_table(html_source, pj, s)  # Ѱ��Ǳ�ڿͻ�
        ele_table_list = driver.find_elements_by_xpath("//html/body/div[1]/table[@class='con_table']")
        is_same_phone = False;
        for idx in range(2, 2 + len(ele_table_list)):
            # ֻɨ���һҳ��
            ele_tmp_phone = get_element(driver, 'xpath', 'html/body/div[1]/table[%s]/tbody/tr[2]/td[7]/p[2]' % idx)
            if not ele_tmp_phone:  # �Ҳ���
                continue
            tmp_phone = ele_tmp_phone.text.strip()
            print u'�ԱȺ���:', tmp_phone, pju.phone
            if tmp_phone == pju.phone:
                is_same_phone = True
                break
        if not is_same_phone:
            print u'�ȽϺ���ʧ�ܣ�������Ϊ������'
            pj.flag = False
            s.add(pj)
            s.commit()
            return
        order_info = get_element(driver, 'xpath', 'html/body/div[1]/table[%s]/tbody/tr[2]/td[9]' % idx).text
        if u'�ܾ�' in order_info:
            print u'�̼Ҿܾ������ñ�־λ'
            log_msg = u'�̼�:' + str(pju.id) + u' ' + str(pju.wangwang) + u' �ܾ��˶���:' + str(pj.id)
            pj.flag = False
            s.add(pj)
            s.commit()
            return
        ele_pingjia = get_element(driver, 'xpath', 'html/body/div[1]/table[%s]/tbody/tr[2]/td[10]/a' % idx)
        # ele_pingjia = get_element(driver, 'xpath', 'html/body/div[1]/table[2]/tbody/tr[2]/td[10]/a')
        if not ele_pingjia:
            return
        if ele_pingjia.text == u'׷������':
            print u'׷�����ۣ����ñ�־λ'
            pj.has_pingjia_flag = True
            s.add(pj)
            s.commit()
            return
            pass
        if ele_pingjia.text != u'����':
            print u'����������', ele_pingjia.text
            # html/body/div[1]/table[2]/tbody/tr[2]/td[9]/text()
            print  get_element(driver, 'xpath', 'html/body/div[1]/table[%s]/tbody/tr[2]/td[9]' % idx).text

            # print  get_element(driver, 'xpath', 'html/body/div[1]/table[%s]/tbody/tr[2]/td[9]/text()' % idx).text
            return
        driver.execute_script("arguments[0].click();", ele_pingjia)
        # ele_pingjia.click()
        time.sleep(3)
        ele_start5 = get_element(driver, 'id', 'star5')
        ele_start5.click()
        try:
            ele_biaoqian = driver.find_element_by_id('perfect')
            ele_biaoqian.click()
        except:
            # û�ҵ�Ԫ�أ�˵��û�б�ǩ
            pass
        comment_list = [c for c in pju.category.comments if c.has_used_flag == False]
        all_cmts_has_used_flag = False
        if len(comment_list) == 0:
            print u'�Զ��岻�ظ������Ѿ����꣬����Ĭ������'
            all_cmts_has_used_flag = True
            comment_list = s.query(Comment).filter(Comment.cid == 0).all()
        choice_comment = random.choice(comment_list)
        if all_cmts_has_used_flag == False and pju.use_own_pingjia:
            print u'���ظ�����!!!!!'
            choice_comment.has_used_flag = True  # ���ͻ�ʹ���Լ������۵�ʱ����������Ѿ��ù��ˣ�����Ҫ�ٴ�������
        comment = choice_comment.content
        cmts_len = len(comment)
        if cmts_len < 51:
            comment += u' ' * (random.randint(120, 150) - cmts_len)
        print comment
        # driver.find_element_by_id('content').send_keys(comment)
        driver.execute_script("document.getElementById('content').value='" + comment + "';")
        time.sleep(1)
        # ele_commit = get_element(driver, 'id', 'pingjiaBtn')
        # ele_commit.click()
        # ������ͼƬ
        # ���жϴ����Ƿ���ͼƬ����ͼ�Ԍ�

        # �İ棬��ʱ��֧��ÿ��̶�����ͼƬ����
        img_upload_succ = False
        img_need_to_del_list = []
        if choice_comment.img_name:
            autoit.WinActivate("[CLASS:Chrome_WidgetWin_1]", "")
            # �ϴ�����ͼƬ
            for idx, img in enumerate(choice_comment.img_name.split('|'), start=1):
                pju_img_path = img_path_driver + 'imgs\\' + str(pju.id) + '\\' + img
                if os.path.exists(pju_img_path):  # ���ͼƬ����
                    print u'��������Ҫ�ϴ�ͼƬ', pju_img_path
                    driver.find_element_by_id('SWFUpload_0').click()
                    # driver.find_element_by_id('SWFUpload_0').send_keys(Keys.ENTER)
                    time.sleep(3)
                    autoit.WinWait(u"��", "", 5)
                    autoit.WinActivate(u"��")
                    autoit.ControlSetText(u"��", "", "[CLASS:Edit; INSTANCE:1]", pju_img_path)
                    time.sleep(1)
                    autoit.ControlClick(u"��", "", "[CLASS:Button; INSTANCE:2]")  # �����ϴ�����
                    # �ж��ϴ��Ƿ����
                    try_cnt = 0
                    while try_cnt < 12:
                        time.sleep(1)
                        try_cnt += 1
                        if get_element(driver, 'id', 'lipic' + str(idx)):
                            img_upload_succ = True
                            img_need_to_del_list.append(pju_img_path)
                            time.sleep(2)
                            break
                    pass
                else:
                    print u'������û������ͼƬ��'
                pass
        # end ���ͼƬ
        driver.execute_script("document.getElementById('pingjiaBtn').click();")
        time.sleep(5)
        # check ����ɹ�
        if driver.page_source.find(u'�����ύ�ɹ�') != -1:
            # �������ݿ�
            pj.has_pingjia_flag = True
            pj.cookies = str(driver.get_cookies())
            # if not cks:
            #     pj.cookies = cks
            pj.user.pingjia_cnt += 1
            pj.user.pingjia_per_day_cnt += 1
            pj.user.last_pingjia_time = time.time() + random.randint(345, 679)
            pj.pj_cmt = choice_comment  # ������������
            if all_cmts_has_used_flag == False and pju.use_own_pingjia:
                s.add(choice_comment)
            if img_upload_succ:
                for img_del in img_need_to_del_list:
                    os.remove(img_del)
                print u'ͼƬ���۳ɹ�:):):):):):):):):):):):):):):):):):):):):):)'
            s.add(pj)
            s.commit()
            #global_adsl.inc_use_cnt()
            print u'���۳ɹ�:):):):):):):):):):):):):):):):):):):):):)'

    except:
        print traceback.print_exc()
        pass
        # driver.delete_all_cookies()
    pass


def schedule_yuyue(s):
    user_list = s.query(User).filter(
        User.flag == True,
        User.yuyue_cnt < User.req_yuyue_cnt,  # �Ѿ�ԤԼ��С��ԤԼ����
        User.yuyue_start_time < time.time(),  # ��ʼʱ�䵽����
        User.last_yuyue_time + User.yuyue_interval + random.randint(157, 678) < time.time(),  # ����ʱ���������Ҽ��������
        User.yuyue_per_day_cnt < User.rdm_yuyue_per_day_cnt,  # ÿ��ԤԼ��С�ڿͻ�ÿ��涨��ԤԼ��
        # User.yuyue_per_day_cnt < User.req_yuyue_cnt / User.req_day_cnt  # ����ԤԼ���Ƿ��ˣ������Ĳż���
    ).order_by(func.random()).all()
    len_user = len(user_list)
    if not len_user:
        print u'��ǰû�з���������ԤԼyy'
        return True
    print u'����ԤԼ������', len_user
    idx_cnt = 0
    for user in user_list:
        if len(user.urls) == 0:
            print user.id, u'û��urls'
            continue
        print
        #global_adsl.reconnect()  # adsl����
        # time.sleep(3)
        idx_cnt += 1
        print datetime.now(), 'Լ��', idx_cnt, '/', len_user, '����:', user.shop_id, user.id, user.qq, user.wangwang, user.company, ',ԭ��Լ:', user.original_yuyue_cnt, '�Ѿ�Լ:', user.yuyue_cnt, ',����Լ��:', user.yuyue_per_day_cnt, ',���컹ҪԼ:', user.rdm_yuyue_per_day_cnt - user.yuyue_per_day_cnt
        # random_url = random.choice([url for url in user.urls if url.flag == True])
        random_url = random.choice(user.urls)
        try:
            m_yuyue(s, user, random_url.href)
        except Exception, e:
            print e
            print traceback.format_exc()
            continue
        # time.sleep(random.randint(1, 5))
        pass
    return False
    pass


def schedule_pingjia(s):
    user_list = s.query(User).filter(
        User.flag == True,
        User.pingjia_cnt < User.req_pingjia_cnt,  # �Ѿ�������С����������
        User.last_pingjia_time + User.pingjia_interval + random.randint(157, 567) < time.time(),  # ����ʱ���������Ҽ��������
        User.pingjia_per_day_cnt < User.rdm_pingjia_per_day_cnt,
        # User.pingjia_per_day_cnt < User.req_pingjia_cnt / User.req_day_cnt  # �����������Ƿ���
    ).order_by(func.random()).all()
    pingjia_list = []  # ������ͳ�ưɣ�һ����һ��һ�����ۣ������ÿ������ۼ��
    zone_timestamp = time.mktime(date.today().timetuple())  # ����0��ʱ���
    current_timestamp = time.time()
    for u in user_list:
        # max_pingjia_per_day = (u.req_pingjia_cnt / u.req_day_cnt) - u.pingjia_per_day_cnt  # Ҫ��ȥ�����Ѿ�������
        # pingjia_per_day_index = 0
        # print u.company
        user_pingjias = u.pingjias
        # print user_pingjias
        # print u'�����'
        if len(user_pingjias) == 0:
            continue
        # random.shuffle(user_pingjias)  # �ȴ��ң���bug
        # print user_pingjias
        up_all_flag = True
        for up in user_pingjias:
            # ���ڽ�������ʱ���������Ĳ����ˣ�����С�ڵ�ǰʱ���ȥ2��Сʱ
            if up.has_pingjia_flag == False and up.yuyue_time > zone_timestamp and up.yuyue_time + 4000 < current_timestamp:
                if up.flag:
                    pingjia_list.append(up)
                    break
                else:
                    up_all_flag = False  # �ڵ����ԤԼ�г���������flagΪfalse�����
                    # pingjia_per_day_index += 1
                    # if pingjia_per_day_index >= max_pingjia_per_day:

            pass
        if not up_all_flag:
            print u.id, u'�ڵ����ԤԼ�г���������flagΪfalse�����'
        pass
    # print u'���������б�'
    # print pingjia_list
    len_pingjia = len(pingjia_list)
    if not len_pingjia:
        print '��ǰû�з�������������'
        return True
    print '��ǰ����������', len_pingjia
    # ����˳��
    random.shuffle(pingjia_list)
    idx_cnt = 0
    # ��ʼ����
    for pj in pingjia_list:
        print
        #global_adsl.reconnect()  # adsl����
        idx_cnt += 1
        pju = pj.user
        print datetime.now(), '��:', pj.id, '��', idx_cnt, '/', len_pingjia, '����:', pju.id, pju.qq, pju.wangwang, pju.company, ',ԭ����:', pju.original_pingjia_cnt, ',�Ѿ���:', pju.pingjia_cnt, ',��������:', pju.pingjia_per_day_cnt, ',���컹Ҫ��:', pju.rdm_pingjia_per_day_cnt - pju.pingjia_per_day_cnt
        try:
            do_pingjia(s, pj)
        except Exception, e:
            print e
            print traceback.format_exc()
            continue
        print datetime.now(), '��������', pju.company
        # time.sleep(random.randint(1, 3))
        pass
    return False
    pass


def find_potential_user(db):
    zone_timestamp = time.mktime(date.today().timetuple())  # ����0��ʱ���
    pingjia_list = db.query(PingJia).filter(
        PingJia.has_find_flag == False,  # ��û���ҹ�
        PingJia.yuyue_time > zone_timestamp  # - 86400  # ʱ����ڽ����賿
    ).order_by(func.random()).all()
    if not pingjia_list:
        print u'��ǰ����������Ѱ��Ǳ�ڿͻ�'
        return True  # û�з���true
    req_session = requests.Session()
    HEADER['Host'] = "order.58.com"
    HEADER['User-Agent'] = random.choice(browser_user_agents)
    for pj in pingjia_list:
        # 'http://order.58.com/buyer/orderlist?rand=1440587862889'
        order_url = order_base_url % str(int(time.time())) + str(random.randint(100, 999))
        try:
            cookies = eval(pj.cookies)
            req_session.cookies.clear()  # �����
            for ck in cookies:
                req_session.cookies.set(ck['name'], ck['value'])
            resp = req_session.get(order_url, headers=HEADER, timeout=10)
        except Exception as e:
            print e
            print u'cookies��¼������order list �е����'
            pj.has_find_flag = True
            db.add(pj)
            db.commit()
            continue
        if 'login' in resp.url:
            print u'cookies ʧЧ�ˣ����ñ�־λ������'
            pj.has_find_flag = True
            db.add(pj)
            db.commit()
            return
        html_source = resp.text
        parse_order_table(html_source, pj, db)
        time.sleep(random.randint(5, 20))
    pass


def parse_order_table(html_source, pj, db):
    bs = BeautifulSoup(html_source, 'html.parser')
    potential_user_table_list = bs.find_all('table', class_='con_table')
    potential_user_cnt = len(potential_user_table_list)
    if potential_user_cnt - 1 <= 0:
        print u'��Ǳ�ڿͻ�'
        pj.has_find_flag = True
        db.add(pj)
        db.commit()
        return
    print u'Ǳ�ڿͻ���', potential_user_cnt - 1, u'��'  # ȥ������
    for pu_table in potential_user_table_list:
        ele_order_time = pu_table.find('span', text=re.compile(u'^�µ�ʱ��'))
        if ele_order_time:
            td_info = pu_table.find('td', class_='bt_06')
            shop = td_info.find('a', attrs={'target': '_blank'})
            shop_href = shop.get('href')
            shop_id = shop_href[shop_href.rfind('/') + 1:]
            tmp_shop = db.query(User).filter(User.shop_id == shop_id).first()
            if tmp_shop:
                print u'���Լ��Ŀͻ�'
                continue
            tmp_shop = db.query(PotentialUser).filter(PotentialUser.shop_id == shop_id).first()
            if tmp_shop:
                print u'�Ѿ������ݿ�����'
                continue
            phone = shop.parent.next_sibling.get_text()
            name = shop.get('title')
            order_time_text = ele_order_time.get_text()
            order_time = order_time_text[order_time_text.find(':') + 1:]
            p_user = PotentialUser()
            p_user.shop_id = shop_id
            p_user.name = name
            p_user.phone = phone
            p_user.order_time = order_time
            db.add(p_user)
            db.commit()
            print u'�ҵ�Ǳ�ڿͻ�', name, phone, order_time
        pass
    # ���������Σ���Ҫ��־�������Ѿ��ҹ���
    pj.has_find_flag = True
    db.add(pj)
    db.commit()
    pass


def find_potential_user_qq(db):
    pu_list = db.query(PotentialUser).filter(
        PotentialUser.qq == None,  # û��qq
    ).order_by(func.random()).all()
    if not pu_list:
        print u'��ǰ����������Ѱ��Ǳ�ڿͻ���qq'
        return True  # û�з���true
    HEADER['Host'] = 'shop.58.com'

    for pu in pu_list:
        shop_url = 'http://shop.58.com/' + pu.shop_id  # + '/product/?PGTID=%s&ClickID=1' % get_pgtid()
        HEADER['Host'] = 'shop.58.com'
        HEADER['User-Agent'] = random.choice(browser_user_agents)
        HEADER['Referer'] = None
        try:
            post_url = BeautifulSoup(requests.get(shop_url, headers=HEADER, timeout=10).text, 'html.parser').find('a',
                                                                                                                  class_='t').get(
                'href')
        except:
            pu.qq = '-1'
            db.add(pu)
            db.commit()
        print post_url
        domain_start = post_url.find('//') + 2
        domain_end = post_url.find('.')
        HEADER['Referer'] = shop_url
        HEADER['Host'] = post_url[domain_start:domain_end] + '.58.com'
        ele_qq_box = BeautifulSoup(requests.get(post_url, headers=HEADER, timeout=10).text, 'html.parser').find('span',
                                                                                                                id='qqWrapBox')
        if ele_qq_box:
            qq_href = ele_qq_box.find('a').get('href')
            qq_resp_text = requests.get(qq_href, timeout=10).text
            qq_tmp = "tuin : '"
            qq_start = qq_resp_text.find(qq_tmp) + len(qq_tmp)
            qq_end = qq_resp_text.find("'", qq_start)
            qq = qq_resp_text[qq_start:qq_end]
            print pu.name, u'��QQ���ǣ�', qq
            pu.qq = qq
        else:
            print pu.name, u'��QQ��'
            pu.qq = '0'
        db.add(pu)
        db.commit()

    pass


def schedule():
    s = Session()
    while True:
        have_no_yy_flag = schedule_yuyue(s)
        have_no_pj_flag = schedule_pingjia(s)
        if have_no_yy_flag and have_no_pj_flag:  # ��û��ԤԼ��Ҳû�����ۣ����ʱ����Ҫ�ҿͻ���
            have_no_pu_flag = find_potential_user(s)
            if have_no_pu_flag:  # ���û��Ǳ�ڿͻ�����Ѱ�����ݿ���Ѱ��Ǳ�ڿͻ���qq
                try:
                    find_potential_user_qq(s)
                except:
                    print u'��ȡǱ���û�QQ���쳣���Ȼ�����'
                pass
            pass
        pass

    s.close()
    pass


# global
#global_adsl = Adsl()
while True:
    try:
        global_y = YunMa()
        #global_y = JikeSms()
    except:
        print u'��ʼ������ƽ̨����'
        #global_adsl.reconnect()
        continue
    break
    pass
# set_driver()
global_s = Session()

if __name__ == '__main__':
    schedule()
    pass
