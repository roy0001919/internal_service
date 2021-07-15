#  -*- coding: UTF-8 -*-

from flask import Blueprint, Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date, datetime
from ..dbmodels.dbOperator import DBoperator
from ..dbmodels.models import Pymt_dtl, CashPymt


class Logic_cashPymt:
    def __init__(self, data):
        self.data = data

    def updateCashPymt(self):
        try:
            sql = ["TRUNCATE TABLE smarteropt.web_fin_pymt_unrec; ",
                "INSERT INTO smarteropt.web_fin_pymt_unrec ( "
                "SELECT a.* "
                "FROM smarteropt.mt_pymt_dtl as a "
                "LEFT JOIN smarteropt.web_fin_cashpymt AS b "
                "ON a.refund_ind = b.refund_ind " 
                "AND a.pymt_order_seq = b.pymt_order_seq "
                "WHERE b.pymt_order_seq IS NULL); "
            ]
            for item in sql:
                print('SQL內容: ', item)
                result = DBoperator(CashPymt).customSQL(item)
                print(result)
        except Exception as e:
            return (jsonify(e), 400)

    def cashPymt_send(self):
        insert_dict = {}
        print(self.data)
        try:
            cashpymt_id = self.data["cashpymt_id"] if self.data["cashpymt_id"] is not None else None
            deposit_date = self.data["deposit_date"] if self.data["deposit_date"] is not None else None
            r_id = self.data["r_id"] if self.data["r_id"] is not None else None
            r_name = self.data["r_name"] if self.data["r_name"] is not None else None
            for row in self.data["data"]:
                # records = DBoperator(Pymt_dtl).dyn_filter_query(row)
                # print(row)
                for key, value in row.items():
                    print(key, value)
                    insert_dict['cashpymt_id'] = str(cashpymt_id)
                    if key == "cust_id": insert_dict['cust_id'] = value
                    if key == "cust_name": insert_dict['cust_name'] = value
                    if key == "pymt_order_id":insert_dict['pymt_order_id'] = value
                    if key == "data_src_date":insert_dict['data_src_date'] = value
                    if key == "store_id":insert_dict['store_id'] = value
                    if key == "store_name":insert_dict['store_name'] = value
                    if key == "pymt_amt":insert_dict['pymt_amt'] = value
                    if key == "pymt_order_seq":insert_dict['pymt_order_seq'] = value
                    if key == "etl_dttm":insert_dict['data_dttm'] = value
                    insert_dict['deposit_date'] = deposit_date
                    insert_dict['r_id'] = str(r_id)
                    insert_dict['r_name'] = str(r_name)
                    if key == "refund_ind": insert_dict['refund_ind'] = value
                print(insert_dict)
                # for r in records:
                #     if cashpymt_id:insert_dict['cashpymt_id'] = str(cashpymt_id)
                #     if r.cust_id:insert_dict['cust_id'] = r.cust_id
                #     if r.cust_name:insert_dict['cust_name'] = r.cust_name
                #     if r.pymt_order_id:insert_dict['pymt_order_id'] = r.pymt_order_id
                #     if r.data_src_date:insert_dict['data_src_date'] = r.data_src_date
                #     if r.store_id:insert_dict['store_id'] = r.store_id
                #     if r.store_name:insert_dict['store_name'] = r.store_name
                #     if r.pymt_amt:insert_dict['pymt_amt'] = str(r.pymt_amt)
                #     if r.pymt_order_seq:insert_dict['pymt_order_seq'] = str(r.pymt_order_seq)
                #     if r.etl_dttm:insert_dict['data_dttm'] = r.etl_dttm
                #     if deposit_date:insert_dict['deposit_date'] = deposit_date
                #     if r_id:insert_dict['r_id'] = str(r_id)
                #     if r_name:insert_dict['r_name'] = str(r_name)
                #     if r.refund_ind:insert_dict['refund_ind'] = r.refund_ind
                DBoperator(CashPymt).merge(insert_dict)
            return "資料送出成功", 200
        except Exception as e:
            print(e)
            return str(e), 411
    # def cashPymt_send(self):
    #     print(self.data)
    #     try:
    #         for row in self.data:
    #             DBoperator(CashPymt).merge(row)
    #             print (row)
    #             print("輸入成功: ", row)
    #         msg = "資料輸入成功, "
    #         print(msg)
    #         self.updateCashPymt()
    #
    #         # sql = ["TRUNCATE TABLE smarteropt.web_fin_pymt_unrec; ",
    #         #     "INSERT INTO smarteropt.web_fin_pymt_unrec ( "
    #         #     "SELECT a.* "
    #         #     "FROM smarteropt.mt_pymt_dtl as a "
    #         #     "LEFT JOIN smarteropt.web_fin_cashpymt AS b "
    #         #     "ON a.refund_ind = b.refund_ind "
    #         #     "AND a.pymt_order_seq = b.pymt_order_seq "
    #         #     "WHERE b.pymt_order_seq IS NULL); "
    #         # ]
    #         # for item in sql:
    #         #     print('SQL內容: ', item)
    #         #     result = DBoperator(CashPymt).customSQL(item)
    #         #     print(result)
    #
    #         msg += "資料已經同步"
    #         print (msg)
    #         print("送出")
    #         resp = {'status':'ok','message': msg}
    #         print (resp)
    #         return (jsonify(resp), 200)
    #     except:
    #         return "cashPymt_send error", 411

    def pymtUnrec_query(self):
        query_dict={}
        print(self.data)
        index = 0
        try:
            records = DBoperator(Pymt_dtl).dyn_filter_query(self.data)
            print(records)
            for r in records:
                print(r.pymt_order_id)
                query_dict.update({index:{
                    "pymt_date": str(r.pymt_date),
                    "pymt_method": r.pymt_method,
                    "credit_card_no": r.credit_card_no,
                    "inv_no": r.inv_no,
                    "remark": r.remark,
                    "auth_code": r.auth_code,
                    "pymt_order_seq": r.pymt_order_seq,
                    "store_id": r.store_id,
                    "store_name": r.store_name,
                    "cust_name": r.cust_name,
                    "cust_id": r.cust_id,
                    "pymt_order_id": r.pymt_order_id,
                    "pymt_amt": str(r.pymt_amt),
                    "refund_ind": r.refund_ind,
                    "data_src_date": str(r.data_src_date),
                    "etl_dttm": str(r.etl_dttm)
                }})
                index += 1
            print(query_dict)
            return query_dict, 200
        except:
            return "pymtUnrec_query error", 411