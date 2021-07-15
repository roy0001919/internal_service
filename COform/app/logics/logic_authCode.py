#  -*- coding: UTF-8 -*-

from flask import Blueprint, Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date, datetime
from .dbOperator import DBoperator
from .models import MailOrder, MailOrder_updated, AuthCode

class Logic_authCode:
    def authCode_send(self, data):
        try:
            for row in data:
                print(row)
                DBoperator(AuthCode).merge(row)
                print("輸入成功: ", row)
            msg = "資料輸入成功, "
            print(msg)

            sql=[
                "UPDATE smarteropt.web_fin_mailorder_updated AS a "
                "INNER JOIN smarteropt.web_fin_authcode AS b "
                "ON a.order_id = b.order_id "
                "SET a.auth_code = b.auth_code_new, "
                "a.req_date = b.req_date, "
                "a.auth_date = b.auth_date, "
                "a.mod_date = b.mod_date, "
                "a.mod_r_id = b.r_id;"
            ]
            for item in sql:
                print('SQL內容: ', item)
                result = DBoperator(AuthCode).customSQL(item)
                print (result)
            msg += "資料已經同步"
            print (msg)
            print ("送出")
            resp = {'status':'ok','message': msg}
            print (resp)
            return resp, 200
        except Exception as e:
            return str(e), 401

        # sql = ["TRUNCATE TABLE smarteropt.web_fin_mailorder_updated; ",
        #     "INSERT INTO smarteropt.web_fin_mailorder_updated( "
	    #         "SELECT * FROM smarteropt.web_fin_mailorder "
        #     "); ",

    # def authCode_send(self,data):
    #     # try:
    #     #     for row in data:
    #     #         DBoperator(AuthCode).merge(row)
    #     #         print (row)
    #     #         print("輸入成功: ", row)
    #     #     # send raw SQL to update the web_fin_pay_unrec table
    #     # except Exception as e:
    #     #     return str(e)
    #     try:
    #         for row in data:
    #             result=DBoperator(AuthCode).merge(row)
    #             print('updating AuthCode: ', result)
    #             result=DBoperator(MailOrder_updated).merge(row)
    #             print('updating MailOrder_updated: ',result)

    #     except Exception as e:
    #         print(e)

    #     # sql = ["TRUNCATE TABLE smarteropt.web_fin_mailorder_updated; ",
    #     #     "INSERT INTO smarteropt.web_fin_mailorder_updated( "
	#     #         "SELECT * FROM smarteropt.web_fin_mailorder "
    #     #     "); ",
    #     sql=[
    #         "UPDATE smarteropt.web_fin_mailorder_updated AS a "
    #         "INNER JOIN smarteropt.web_fin_authcode AS b "
    #         "ON a.order_id = b.order_id "
    #         "SET a.auth_code = b.auth_code_new, "
	#         "a.req_date = b.req_date, "
	#         "a.auth_date = b.auth_date, "
    #         "a.mod_date = b.mod_date, "
    #         "a.mod_r_id = b.r_id;"
    #     ]
    #     for item in sql:
    #         try:
    #             print('SQL內容: ', item)
    #             msg = DBoperator(AuthCode).customSQL(item)
    #             print(msg)
    #         except Exception as e:
    #             return str(e)

    def authCode_query(self):
        data={}
        store = request.form.get('store')
        pymt_method = request.form.get('pymt_method')
        date_start = request.form.get('req_date_start')
        date_end = request.form.get('req_date_end')
        cust_id = request.form.get('cust_id')
        payway = request.form.get('payway')
        con1 = cust_id != ''
        con2 = date_start != '' and date_end !=''



        if store != '':
            data['store_id']=store
        if cust_id !='':
            data['cust_id']=cust_id
        if date_start !='' and date_end !='':
            data['req_date']=[date_start, date_end]
        if payway != 'pay_all':
            data['payway']=payway
        for key,value in data.items():
            print(key, value)
        records = DBoperator(MailOrder_updated).dyn_filter_query(data)
        return records
        # elif pymt_method == 'credit':
        #     data['pymt_method']='信用卡'
        #     if store != '':
        #         data['store_id']=store
        #     if cust_id !='':
        #         data['cust_id']=cust_id
        #     if date_start !='' and date_end !='':
        #         data['data_src_date'] = [date_start,date_end]
            
        #     records = DBoperator(Pymt_dtl).dyn_filter_query(data)
        #     return records

