# encoding:utf-8
from selenium.webdriver.common.by import By

HEADER = {
    "Host": "bj.58.com",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
}
by_types = {'id': By.ID, 'class': By.CLASS_NAME, 'link_text': By.LINK_TEXT, 'tag': By.TAG_NAME, 'xpath': By.XPATH}
pingjia_url = 'http://my.58.com/pro/buyordermgr'
order_base_url = 'http://order.58.com/buyer/orderlist?rand=%s'
days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
mobile_user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
    'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.2.1; zh-cn; AMOI N828 Build/JOP40D) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.4 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.2.1; zh-cn; AMOI N828 Build/JOP40D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24; 360browser(securitypay,securityinstalled)',
    'Mozilla/5.0 (Linux; U; Android 4.2.1; zh-CN; AMOI N828 Build/JOP40D) AppleWebKit/534.31 (KHTML, like Gecko) UCBrowser/9.2.4.329 U3/0.8.0 Mobile Safari/534.31',
    'Mozilla/5.0 (Linux; Android 4.2.1; AMOI N828 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.59 Mobile Safari/537.36',
    'Mozilla/5.0 (Android; Mobile; rv:23.0) Gecko/23.0 Firefox/23.0',
    'Mozilla/5.0 (Linux; U; Android 4.2.1; zh-cn; AMOI N828 Build/JOP40D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 SogouMSE/1.2.1',
    'Mozilla/5.0 (Linux; Android 4.2.1; AMOI N828 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.64 Mobile Safari/537.36'

]
browser_user_agents=[
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
]
xing = [u'李', u'王', u'张', u'刘', u'陈', u'杨', u'赵', u'黄', u'周', u'吴', u'徐', u'孙', u'胡', u'朱', u'高', u'林', u'何', u'郭',
        u'马', u'罗', u'梁', u'宋', u'郑', u'谢', u'韩', u'唐', u'冯', u'于', u'董', u'萧', u'程', u'曹', u'袁', u'邓', u'许', u'傅',
        u'沈', u'曾', u'彭', u'吕', u'苏', u'卢', u'蒋', u'蔡', u'贾', u'丁', u'魏', u'薛', u'叶', u'阎', u'余', u'潘', u'杜', u'戴',
        u'夏', u'钟', u'汪', u'田', u'任', u'姜', u'范', u'方', u'石', u'姚', u'谭', u'廖', u'邹', u'熊', u'金', u'陆', u'郝', u'孔',
        u'白', u'崔', u'康', u'毛', u'邱', u'秦', u'江', u'史', u'顾', u'侯', u'邵', u'孟', u'龙', u'万', u'段', u'漕', u'钱', u'汤',
        u'尹', u'黎', u'易', u'常', u'武', u'乔', u'贺', u'赖', u'龚', u'文', u'庞', u'樊', u'兰', u'殷', u'施', u'陶', u'洪', u'翟',
        u'安', u'颜', u'倪', u'严', u'牛', u'温', u'芦', u'季', u'俞', u'章', u'鲁', u'葛', u'伍', u'韦', u'申', u'尤', u'毕', u'聂',
        u'丛', u'焦', u'向', u'柳', u'邢', u'路', u'岳', u'齐', u'沿', u'梅', u'莫', u'庄', u'辛', u'管', u'祝', u'左', u'涂', u'谷',
        u'祁', u'时', u'舒', u'耿', u'牟', u'卜', u'路', u'詹', u'关', u'苗', u'凌', u'费', u'纪', u'靳', u'盛', u'童', u'欧', u'甄',
        u'项', u'曲', u'成', u'游', u'阳', u'裴', u'席', u'卫', u'查', u'屈', u'鲍', u'位', u'覃', u'霍', u'翁', u'隋', u'植', u'甘',
        u'景', u'薄', u'单', u'包', u'司', u'柏', u'宁', u'柯', u'阮', u'桂', u'闵', u'欧阳', u'解', u'强', u'柴', u'华', u'车', u'冉',
        u'房', u'边', u'辜', u'吉', u'饶', u'刁', u'瞿', u'戚', u'丘', u'古', u'米', u'池', u'滕', u'晋', u'苑', u'邬', u'臧', u'畅',
        u'宫', u'来', u'嵺', u'苟', u'全', u'褚', u'廉', u'简', u'娄', u'盖', u'符', u'奚', u'木', u'穆', u'党', u'燕', u'郎', u'邸',
        u'冀', u'谈', u'姬', u'屠', u'连', u'郜', u'晏', u'栾', u'郁', u'商', u'蒙', u'计', u'喻', u'揭', u'窦', u'迟', u'宇', u'敖',
        u'糜', u'鄢', u'冷', u'卓', u'花', u'仇', u'艾', u'蓝', u'都', u'巩', u'稽', u'井', u'练', u'仲', u'乐', u'虞', u'卞', u'封',
        u'竺', u'冼', u'原', u'官', u'衣', u'楚', u'佟', u'栗', u'匡', u'宗', u'应', u'台', u'巫', u'鞠', u'僧', u'桑', u'荆', u'谌',
        u'银', u'扬', u'明', u'沙', u'薄', u'伏', u'岑', u'习', u'胥', u'保', u'和', u'蔺']
ming = [u'先生', u'女士', u'经理', u'师傅', u'小姐', u'主管']
