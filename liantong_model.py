# encoding:utf-8

import sys, time
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

reload(sys)
sys.setdefaultencoding('utf-8')
# engine = create_engine('mysql+pymysql://root:root@100.96.141.6:3306/yuyue?charset=utf8', echo=False)
# engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/yuyue?charset=utf8', echo=False)

engine = create_engine("sqlite:///liantong.sqlite", echo=False)
# engine.raw_connection().connection.text_factory = str

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Category(Base):
    # 行业
    __tablename__ = 'categorys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    users = relationship('User', backref='category')  # 该行业对应的用户
    comments = relationship('Comment', backref='category')  # 该行业对应的评语

    def __init__(self, name):
        self.name = name
        pass

    def __repr__(self):
        return '<Category:' + self.name + '>'
        pass

    pass


class Comment(Base):
    # 评语,一个行业有n个评语
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(Integer, ForeignKey('categorys.id'))
    has_used_flag = Column(Boolean, server_default=text('0'))  # 标志位，是否已经用过
    img_name = Column(String(20))  # 图片名称，后缀可能是png 或者jpg
    content = Column(Text)  # 内容
    pj = relationship("PingJia", uselist=False, backref="pj_cmt")  # 评价内容和评价是一对一关系，有的评价有评价内容，有的没有

    def __repr__(self):
        return '<Comment:' + str(self.id) + '>'

    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qq = Column(String(20))  # 旺旺名称
    wangwang = Column(String(20))  # 旺旺名称
    company = Column(String(50))  # 公司名称
    flag = Column(Boolean, server_default=text('1'))  # 标志位，默认是True正常
    req_content = Column(Text)  # 客户要求概述

    yuyue_cnt = Column(Integer, server_default=text('0'))  # 预约数
    req_yuyue_cnt = Column(Integer, server_default=text('10'))  # 要求预约数
    yuyue_per_day_cnt = Column(Integer, server_default=text('0'))  # 每天的预约数，新的一天会清零
    rdm_yuyue_per_day_cnt = Column(Integer, server_default=text('10'))  # 每天要求的随机预约数
    req_yuyue_per_day_cnt = Column(Integer, server_default=text('10'))  # 每天要求的预约数
    original_yuyue_cnt = Column(Integer, server_default=text('0'))  # 客户原有预约数
    yuyue_interval = Column(Integer, server_default=text('666'))  # 预约间隔，单位为秒
    last_yuyue_time = Column(Float, server_default=text('0'))  # 上次预约时间，和间隔配合用

    pingjia_cnt = Column(Integer, server_default=text('0'))  # 评价数
    req_pingjia_cnt = Column(Integer, server_default=text('0'))  # 要求评价数
    pingjia_per_day_cnt = Column(Integer, server_default=text('0'))  # 每天的评价数，新的一天会清零
    rdm_pingjia_per_day_cnt = Column(Integer, server_default=text('10'))  # 每天要求的随机评价数
    req_pingjia_per_day_cnt = Column(Integer, server_default=text('10'))  # 每天要求的评价数
    original_pingjia_cnt = Column(Integer, server_default=text('0'))  # 客户原有评价数
    pingjia_interval = Column(Integer, server_default=text('666'))  # 评价间隔，单位为秒
    last_pingjia_time = Column(Float, server_default=text('0'))  # 上次评价时间，和间隔配合用
    use_own_pingjia = Column(Boolean, server_default=text('0'))  # 使用自己的评价

    # req_day_cnt = Column(Integer, server_default=text('1'))  # 要求天数

    cid = Column(Integer, ForeignKey('categorys.id'))
    yuyue_start_time = Column(Float, server_default=text('0'))  # 预约开始时间，不至于开始的时候就全开始，用sql语句生成

    # web_domain = Column(String(10), server_default=text('bj'))  # 哪个省份，只记录省份，然后拼接
    # web_cate = Column(String(10))  # 行业，然后拼接
    # name = Column(String(10))
    phone = Column(String(20))
    shop_id = Column(String(20))

    urls = relationship('Url', backref='user')  # 该用户的所有的对应的url
    pingjias = relationship('PingJia', backref='user')  # 该用户所有的预约成功的手机号

    def __repr__(self):
        return '<User:{company:' + self.company.encode() + ' phone:' + self.phone + '}>'
        pass


class PotentialUser(Base):  # 潜在客户
    __tablename__ = 'potential_users'
    shop_id = Column(String(20), primary_key=True)
    name = Column(String(20))
    phone = Column(String(20))
    qq = Column(String(20))
    order_time = Column(String(20))
    flag = Column(Boolean, server_default=text('1'))  # 该评价可用标志位，注意和是否评价标志位区分

    pass


class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('users.id'))
    href = Column(String(100))
    # flag = Column(Boolean, server_default=text('1'))  # 现在的预约数不是总数了，是针对每个url的

    def __init__(self, href=''):
        self.href = href
        pass

    pass


class MyProxy(Base):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy = Column(String(20))
    use_cnt = Column(Integer, default=0, server_default=text('0'))  # 使用次数

    def __repr__(self):
        return '<Proxy:' + self.proxy + '>'


class PingJia(Base):
    # 预约成功的手机号码，记录预约时间，是否评价，是否追加评价，cookies
    __tablename__ = 'pingjias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('users.id'))
    user_name = Column(String(15))  # 预约成功的用户名
    phone = Column(String(15))  # 预约成功的电话
    yuyue_time = Column(Float, default=time.time())  # 预约时间，大于2个小时的才能够确认订单
    cookies = Column(Text)  # 每个手机号对应一个cookies，在预约的时候，浏览器add cookies 直接免登陆
    flag = Column(Boolean, server_default=text('1'))  # 该评价可用标志位，注意和是否评价标志位区分
    has_pingjia_flag = Column(Boolean, server_default=text('0'))  # 是否评价标志位，
    has_find_flag = Column(Boolean, server_default=text('0'))  # 是否已经用来找过客户标志位，

    cmt_id = Column(Integer, ForeignKey('comments.id'))  # 评价内容，对应评价内容上，查询时候有利于看到哪个评价了

    def __repr__(self):
        # str(datetime.fromtimestamp(self.yuyue_time)) +
        return '<PingJia:' + self.user_name + ' ' + self.phone + '>'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    pass
