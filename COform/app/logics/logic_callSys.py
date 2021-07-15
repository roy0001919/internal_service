from flask import Blueprint, Flask, render_template, redirect, url_for, flash, session, request, jsonify, make_response, send_file
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date, datetime
from .dbOperator import DBoperator
from .models import CallSys_Cust, CallSys_lastStatus, CallSys_records 
import csv, io, os

class Logic_CallSys:
    def callSys_query(data):

        try:
            records = DBoperator(CallSys_lastStatus).dyn_filter_query(data)
            print('查詢結果: ', records)
            return records
        except Exception as e:
            print('查詢錯誤: ', e)
            return str(e), 401
        
        # if bool(request.form.getlist('cust_name_chk')): data['cust_name']=self.formValue('cust_name')
        # if bool(request.form.getlist('cust_phone_chk')): data['cust_phone']=self.formValue('cust_phone')
        # if bool(request.form.getlist('last_send_date_chk')): data['last_send_date']=[self.formValue('last_send_date_start'), self.formValue('last_send_date_end')]
        # if bool(request.form.getlist('last_call_date_chk')): data['last_call_date']=[self.formValue('last_call_date_start'), self.formValue('last_call_date_end')]
        # if bool(request.form.getlist('call_cnt_chk')): data['call_cnt']=[self.formValue('call_cnt_start'), self.formValue('call_cnt_end')]

        # try:
        #     result = DBoperator(CallSys_lastStatus).dyn_filter_query(data)
        #     print('查詢結果: ', result)
        #     return result
        # except Exception as e:
        #     print('查詢錯誤: ', e)
        #     return str(e)

    def formValue(self, *arg):
        result=""
        for a in arg:
            elem = request.form.get(a)
            if elem :
                result += elem
            else:
                return None
        return result