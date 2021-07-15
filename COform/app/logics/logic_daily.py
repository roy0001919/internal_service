#  -*- coding: UTF-8 -*-

from flask import Blueprint, Flask, render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date, datetime
from ..dbmodels.dbOperator import DBoperator
from ..dbmodels.models import DailyRPT
# from .common import storeIndex

class Logic_daily:
    def __init__(self, data):
        self.data = data

    def daily_send(self):
        print(self.data)
        # today = datetime.utcnow()
        # dailyDict={}
        # dailyDict['r_name'] = current_user.username
        # dailyDict['r_id'] = current_user.id
        # dailyDict['store_id'] = request.form.get('store')
        # dailyDict['store_name'] = storeIndex[dailyDict['store_id']]
        # dailyDict['r_date'] = request.form.get('input_date')
        # dailyDict['on_duty'] = request.form.get('on_duty')
        # dailyDict['on_duty_name'] = request.form.get('on_duty_name')
        # dailyDict['item_num'] = request.form.get('store')[:2]+today.strftime('%Y%m%d%H%M%S')
        return DBoperator(DailyRPT).insert(self.data)
        # today = datetime.utcnow()
        # dailyDict={}
        # dailyDict['r_name'] = current_user.username
        # dailyDict['r_id'] = current_user.id
        # dailyDict['store_id'] = request.form.get('store')
        # dailyDict['store_name'] = storeIndex[dailyDict['store_id']]
        # dailyDict['r_date'] = request.form.get('input_date')
        # dailyDict['on_duty'] = request.form.get('on_duty')
        # dailyDict['on_duty_name'] = request.form.get('on_duty_name')
        # dailyDict['item_num'] = request.form.get('store')[:2]+today.strftime('%Y%m%d%H%M%S')
        # for i in dailyDict:
        #     print(i, dailyDict[i])
        #     # print(dailyDict.values())
        #     # print(type(dailyDict.values()))
        #
        # if '' in dailyDict.values():
        #     message = "有欄位未填，請確實填寫"
        #     flash(message)
        #     print(message)
        # else:
        #     dateStr = dailyDict['r_date']
        #     dateObj = datetime.strptime(dateStr, '%Y-%m-%d')
        #     datediff = (today-dateObj).days
        #     # dateSubmit = dateStr(dailyDict['r_date'])
        #     # datediff = (today-dateSubmit).days
        #     print(datediff, type(datediff))
        #     if datediff<0 or datediff > 2:
        #         message = "日期錯誤! 輸入日期不能大於今天或超過兩天前!"
        #         flash(message)
        #         print (message)
        #     else:
        #         message="資料輸入:"
        #         flash(message)
        #         print(message)
        #         DBoperator(DailyRPT).insert(dailyDict)
        #         flash('成功')



    def daily_lastTen(self):
        print('searching')
        store = request.form.get('store')
        records = DBoperator(DailyRPT).retrieve(store)
        return records
        # return ('',204)
