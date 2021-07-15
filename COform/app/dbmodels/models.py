
#  -*- coding: UTF-8 -*-

from flask_login import UserMixin
from . import models_bp, db
# from .. import db, app

db.metadata.clear()

class Pymt_dtl(db.Model):
    __tablename__ = 'web_fin_cashpymt_unrec'

    cust_id = db.Column('cust_id', db.String(30), nullable=True)
    cust_name = db.Column('cust_name', db.String(50), nullable=True)
    pymt_order_id = db.Column('pymt_order_id', db.String(20), nullable=True)
    data_src_date = db.Column('data_src_date', db.DateTime, nullable=True)
    store_id = db.Column('store_id', db.String(20), nullable=True)
    store_name = db.Column('store_name', db.String(50), nullable=True)
    pymt_method = db.Column('pymt_method', db.String(50), nullable=True)
    pymt_amt = db.Column('pymt_amt', db.DECIMAL(24,0), nullable=True)
    credit_card_no = db.Column('credit_card_no', db.String(20), nullable=True)
    auth_code = db.Column('auth_code', db.String(20), nullable=True)
    inv_no = db.Column('inv_no', db.String(20), nullable=True)
    remark = db.Column('remark', db.String(255), nullable=True)
    pymt_order_seq = db.Column('pymt_order_seq', db.String(30), primary_key = True)
    pymt_date = db.Column('pymt_date', db.DateTime, nullable=True)
    refund_ind = db.Column('refund_ind', db.String(1), nullable=True)
    etl_dttm = db.Column('etl_dttm', db.DateTime, nullable=True)


    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class CashPymt(db.Model):
    __tablename__ = 'web_fin_cashpymt_paid'

    cashpymt_id = db.Column('cashpymt_id', db.String(50), nullable=False)
    cust_id = db.Column('cust_id', db.String(30), nullable=True)
    cust_name = db.Column('cust_name', db.String(50), nullable=True)
    pymt_order_id = db.Column('pymt_order_id', db.String(30), nullable=True)
    # pymt_order_id = db.Column(db.String(30), db.ForeignKey('web_fin_pymt_unrec.pymt_order_id'), nullable=False)
    data_src_date = db.Column('data_src_date', db.DateTime, nullable=True)
    store_id = db.Column('store_id', db.String(20), nullable=True)
    store_name = db.Column('store_name', db.String(50), nullable=True)
    pymt_amt = db.Column('pymt_amt', db.DECIMAL(24,0), nullable=True)
    pymt_order_seq = db.Column('pymt_order_seq', db.String(30), primary_key=True)
    data_dttm = db.Column('data_dttm', db.DateTime, nullable=False)
    deposit_date = db.Column('deposit_date', db.DateTime, nullable=False)
    r_id = db.Column('r_id', db.String(20), nullable=False)
    r_name = db.Column('r_name', db.String(20), nullable=False)
    refund_ind = db.Column('refund_ind', db.String(1), nullable=True)




    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class MailOrder(db.Model):
    __tablename__ = 'web_fin_mailorder'

    mod_r_id = db.Column ('mod_r_id', db.String(6), nullable = False)
    mod_date = db.Column('mod_date', db.DateTime, nullable = False)
    status = db.Column('status', db.String(6), nullable=False)
    order_id = db.Column('order_id', db.Integer, primary_key = True)
    store_id = db.Column ('store_id', db.String(50), nullable = True)
    store_name = db.Column ('store_name', db.String(50), nullable = True)
    r_id = db.Column('r_id', db.String(50), nullable = True)
    r_name = db.Column('r_name', db.String(50), nullable = True)
    auth_code = db.Column ('auth_code', db.String(50), nullable = True)
    auth_date = db.Column ('auth_date', db.DateTime, nullable = True)
    req_date = db.Column ('req_date', db.DateTime, nullable = True)
    card_holder = db.Column ('card_holder', db.String(50), nullable = True)
    cust_name = db.Column ('cust_name', db.String(50), nullable = True)
    cust_id = db.Column ('cust_id', db.String(50), nullable = True)
    card_num = db.Column ('card_num', db.String(50), nullable = True)
    last3 = db.Column ('last3', db.String(50), nullable = True)
    bank = db.Column ('bank', db.String(50), nullable = True)
    card_exp = db.Column ('card_exp', db.DateTime, nullable = True)
    payway = db.Column ('payway', db.String(50), nullable = True)
    amount = db.Column ('amount', db.String(50), nullable = True)
    bank_req_date = db.Column ('bank_req_date', db.DateTime, nullable = True)
    signature = db.Column ('signature', db.Text, nullable = False)
    # datetime_stamp = db.Column ('datetime_stamp', db.DateTime, nullable = True)
    
# prepare to pass a set of arguments

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class MailOrder_mods(db.Model):
    __tablename__ = 'web_fin_mailorder_mods'

    mod_id = db.Column('mod_id', db.String(100), nullable = False)
    mod_id_seq = db.Column('mod_id_seq', db.String(20), primary_key=True)
    coform_id = db.Column('coform_id', db.String(100), nullable = False)
    status = db.Column('status', db.String(6), nullable=False)
    auth_code = db.Column ('auth_code', db.String(50), nullable = False)
    auth_date = db.Column ('auth_date', db.DateTime, nullable = False)
    req_date = db.Column ('req_date', db.DateTime, nullable = False)
    bank_req_date = db.Column ('bank_req_date', db.DateTime, nullable = False)
    mod_r_id = db.Column ('mod_r_id', db.String(6), nullable = False)
    mod_date = db.Column('mod_date', db.DateTime, nullable = False)
    # datetime_stamp = db.Column ('datetime_stamp', db.DateTime, nullable = True)
    
# prepare to pass a set of arguments

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class MailOrder_updated(db.Model):
    __tablename__ = 'web_fin_mailorder_updated'

    order_id = db.Column('order_id', db.Integer, primary_key = True)
    store_id = db.Column ('store_id', db.String(50), nullable = True)
    store_name = db.Column ('store_name', db.String(50), nullable = True)
    r_id = db.Column('r_id', db.String(50), nullable = True)
    r_name = db.Column('r_name', db.String(50), nullable = True)
    auth_code = db.Column ('auth_code', db.String(50), nullable = True)
    auth_date = db.Column ('auth_date', db.DateTime, nullable = True)
    req_date = db.Column ('req_date', db.DateTime, nullable = True)
    card_holder = db.Column ('card_holder', db.String(50), nullable = True)
    cust_name = db.Column ('cust_name', db.String(50), nullable = True)
    cust_id = db.Column ('cust_id', db.String(50), nullable = True)
    card_num = db.Column ('card_num', db.String(50), nullable = True)
    # cb_3in1 = db.Column ('cb_3in1', db.String(50), nullable = True)
    last3 = db.Column ('last3', db.String(50), nullable = True)
    bank = db.Column ('bank', db.String(50), nullable = True)
    card_exp = db.Column ('card_exp', db.DateTime, nullable = True)
    payway = db.Column ('payway', db.String(50), nullable = True)
    # phone_day = db.Column ('phone_day', db.String(50), nullable = True)
    # phone_night = db.Column ('phone_night', db.String(50), nullable = True)
    # recept_type = db.Column ('recept_type', db.String(50), nullable = True)
    # recept_num = db.Column ('recept_num', db.String(50), nullable = True)
    # vat_num = db.Column ('vat_num', db.String(50), nullable = True)
    # vat_title = db.Column ('vat_title', db.String(50), nullable = True)
    amount = db.Column ('amount', db.String(50), nullable = True)
    signature = db.Column ('signature', db.Text, nullable = False)
    status = db.Column('status', db.String(100))
    mod_date = db.Column('mod_date', db.DateTime)
    mod_r_id = db.Column('mod_r_id', db.String(50))
    bank_req_date = db.Column ('bank_req_date', db.DateTime, nullable = True)
    # datetime_stamp = db.Column ('datetime_stamp', db.DateTime, nullable = True)
    
# prepare to pass a set of arguments

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class AuthCode(db.Model):
    __tablename__ = 'web_fin_authcode'

    order_id = db.Column('order_id', db.Integer, primary_key = True)
    store_id = db.Column ('store_id', db.String(50), nullable = True)
    store_name = db.Column ('store_name', db.String(50), nullable = True)
    r_id = db.Column('r_id', db.String(50), nullable = True)
    r_name = db.Column('r_name', db.String(50), nullable = True)
    auth_code = db.Column ('auth_code', db.String(50), nullable = True)
    auth_code_new = db.Column ('auth_code_new', db.String(50), nullable = True)
    auth_date = db.Column ('auth_date', db.DateTime, nullable = True)
    mod_date = db.Column ('mod_date', db.DateTime, nullable = True)
    req_date = db.Column ('req_date', db.DateTime, nullable = True)
    cust_name = db.Column ('cust_name', db.String(50), nullable = True)
    cust_id = db.Column ('cust_id', db.String(50), nullable = True)
    amount = db.Column ('amount', db.String(50), nullable = True)
    # datetime_stamp = db.Column ('datetime_stamp', db.DateTime, nullable = True)
    
# prepare to pass a set of arguments

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

    #def __init__(self, order_id, r_name, r_id, req_date, auth_date, mem_bday, card_exp, store, bank, auth_code, card_num, )

class DailyRPT(db.Model):
    __tablename__ = 'web_sales_dailyrpt'

    item_num        = db.Column('item_num', db.String(50), primary_key = True)
    r_name          = db.Column('r_name', db.String(50), nullable = False)
    r_id            = db.Column('r_id', db.String(50), nullable = False)
    store_id        = db.Column('store_id', db.String(50), nullable = False)
    store_name      = db.Column('store_name', db.String(50), nullable = False)
    r_date          = db.Column('r_date', db.DateTime, nullable = False)
    on_duty         = db.Column('on_duty', db.Float, nullable = False)
    on_duty_name    = db.Column('on_duty_name', db.String(100), nullable = False)
    datetimestamp   = db.Column('datetimestamp', db.DateTime, nullable = False)
    mod_id          = db.Column('mod_id', db.String(50), nullable = False)    
    mod_date        = db.Column('mod_date', db.DateTime, nullable = False)


# prepare to pass a set of arguments

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")
    
# class User(UserMixin, db.Model):
#
#     __tablename__ = 'web_hr_emp'
#
#     id = db.Column(db.String(6), primary_key = True)
#     # public_id = db.Column(db.String(50), unique=True)
#     username = db.Column(db.String(50), nullable = False)
#     roles = db.Column('depart_name',db.String(50), nullable = False)


    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")
            
    def get_role(self):
        return self.roles


class NameList(db.Model):
    __tablename__ = 'web_mktg_name_list'

    cust_name = db.Column('cust_name', db.String(50), nullable = True)
    cust_phone = db.Column('cust_phone', db.String(50), nullable = True)
    cust_address = db.Column('cust_address', db.String(50), nullable = True)
    cust_email = db.Column('cust_email', db.String(50), nullable = True)
    campaign_id = db.Column('campaign_id', db.String(50), nullable = True)
    form_date = db.Column('form_date', db.DateTime, nullable = True)
    visit_id = db.Column('visit_id', db.String(50), primary_key = True)
    cust_gid = db.Column('cust_gid', db.String(50), nullable = False)
    send_date = db.Column('send_date', db.DateTime, nullable = True)
    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class CallSys_Cust(db.Model):
    __tablename__ = 'web_callsys_cust'

    cust_phone = db.Column('cust_phone', db.String(50), primary_key = True)
    cust_name = db.Column('cust_name', db.String(50), nullable = True)
    cust_address = db.Column('cust_address', db.String(50), nullable = True)
    cust_email = db.Column('cust_email', db.String(50), nullable = True)
    last_status = db.Column('last_status', db.String(50), nullable = True)
    form_date = db.Column('form_date', db.DateTime, nullable = True)
    send_date = db.Column('send_date', db.DateTime, nullable = True)
    call_cnt = db.Column('call_cnt', db.String(11), nullable = True)
    last_call_date = db.Column ('last_call_date', db.DateTime, nullable = True)
    cust_gid = db.Column('cust_gid', db.String(50), nullable = False)
    src_campaign_id = db.Column('src_campaign_id', db.String(100), nullable = True)
    last_campaign_id = db.Column('last_campaign_id', db.String(100), nullable = True)

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class CallSys_records(db.Model):
    __tablename__ = 'web_callsys_call_records'

    cust_phone = db.Column('cust_phone', db.String(50), primary_key = True)
    call_seq = db.Column('call_seq', db.String(50), nullable = False)
    call_date = db.Column('call_date', db.DateTime, nullable = True)
    call_staff = db.Column('call_staff', db.String(10), nullable = True)
    call_status = db.Column('call_status', db.String(50), nullable = True)
    call_memo = db.Column('call_memo', db.String(255), nullable = True)
    call_campaign_id = db.Column('call_campaign_id', db.String(50), nullable = False)


    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class CallSys_lastStatus(db.Model):
    __tablename__ = 'web_callsys_last_status'

    cust_name = db.Column('cust_name', db.String(50), nullable = False)
    cust_phone = db.Column('cust_phone', db.String(50), primary_key=True)
    call_cnt = db.Column('call_cnt', db.String(11), nullable = True)
    last_call_date = db.Column('last_call_date', db.DateTime, nullable = True)
    last_status = db.Column('last_status', db.String(50), nullable = True)
    last_call_staff = db.Column('last_call_staff', db.String(10), nullable = True)
    last_campaign_id = db.Column('last_campaign_id', db.String(100), nullable = True)
    last_send_date = db.Column('last_send_date', db.DateTime, nullable = True)
    

    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")

class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column('id', db.Integer, primary_key = True)
    password = db.Column('password', db.String(128), nullable = False)
    last_login = db.Column('last_login', db.DateTime, nullable = True)
    is_superuser = db.Column('is_superuser', db.Integer, nullable = False)
    username = db.Column('username', db.String(150), nullable=False)
    first_name = db.Column('first_name', db.String(150), nullable=False)
    last_name = db.Column('last_name', db.String(150), nullable=False)
    email = db.Column('email', db.String(254), nullable=False)
    is_staff = db.Column('is_staff', db.Integer, nullable=False)
    is_active = db.Column('is_active', db.Integer, nullable=False)
    date_joined = db.Column('date_joined', db.DateTime, nullable=False)


    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")


class WebHrEmp(db.Model):
    __tablename__ = 'web_hr_emp'

    id = db.Column('id', db.String(12), primary_key = True)
    jobstatus = db.Column('jobstatus', db.String(12), nullable = True)
    username = db.Column('username', db.String(50), nullable = True)
    depart_name = db.Column('depart_name', db.String(50), nullable = True)


    def __init__ (self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except TypeError:
            print("資料庫的值錯誤，請重新確認")