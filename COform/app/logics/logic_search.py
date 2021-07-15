#  -*- coding: UTF-8 -*-

from flask import request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date, datetime
from ..dbmodels.dbOperator import DBoperator
from ..dbmodels.models import MailOrder, MailOrder_updated, AuthCode, DailyRPT, CashPymt
import csv, os
from io import StringIO
import ast
import threading
from flask import current_app
# from ..app import app


# app = current_app._get_current_object()


class Logic_search:

    def __init__(self, data):
        self.data = data

    # def query_daily(self):
    #     data={}
    #     if bool(request.form.getlist('store_chk')): data['store_id']=self.formValue('store')
    #     if bool(request.form.getlist('date_chk')): data['r_date']=[self.formValue('date_start'), self.formValue('date_end')]
    #     if bool(request.form.getlist('r_id_chk')): data['r_id'] = self.formValue('r_id')
    #     # for key, value in data.items():
    #     #     print(key, value)
    #     # return data
    #     try:
    #         result = DBoperator(DailyRPT).dyn_filter_query(self.data)
    #         print ("查詢結果",result)
    #         index = 0
    #         query_dict = {}
    #         for r in result:
    #             query_dict.update({index: {
    #                 "item_num": r.item_num,
    #                 "store_id": r.store_id,
    #                 "store_name": r.store_name,
    #                 # "r_date": r.r_date,
    #                 "on_duty": r.on_duty,
    #                 "on_duty_name": r.on_duty_name,
    #                 "r_id": r.r_id,
    #                 "r_name": r.r_name
    #         }})
    #         print(query_dict)
    #         return query_dict, 200
    #     except:
    #         return "error"

    def query_cashPymt(self):
        # print(self.data)
        data={}
        if bool(request.form.getlist('store_chk')): data['store_id']=self.formValue('store')
        if bool(request.form.getlist('deposit_date_chk')): data['deposit_date']=[self.formValue('deposit_date_start'), self.formValue('deposit_date_end')]
        if bool(request.form.getlist('cust_name_chk')): data['cust_name'] = self.formValue('cust_name')
        if bool(request.form.getlist('pay_date_chk')): data['data_src_date'] = [self.formValue('pay_date_start'), self.formValue('pay_date_end')]


        try:
            results = DBoperator(CashPymt).dyn_filter_query(self.data)
            # print("查詢結果", results)
            index = 0
            query_dict = {}
            for r in results:
                # print(r)
                query_dict.update({index: {
                    "cashpymt_id": r.cashpymt_id,
                    "store_id": r.store_id,
                    "store_name": r.store_name,
                    "cust_id": r.cust_id,
                    "cust_name": r.cust_name,
                    "data_src_date": str(r.data_src_date),
                    "pymt_order_id": r.pymt_order_id,
                    "pymt_order_seq": r.pymt_order_seq,
                    "pymt_amt": str(r.pymt_amt),
                    "deposit_date": str(r.deposit_date),
                    "r_id": r.r_id,
                    "r_name": r.r_name,
                    "data_dttm": str(r.data_dttm)
                }})
                index += 1
            # print(query_dict)
            return query_dict, 200
        except:
            return "query cashpymt function of Logics failed", 411

    def query_mailOrder(self):
        print("query_mailOrder")
        data={}

        if bool(request.form.getlist('store_chk')): data['store_id']=self.formValue('store')
        if bool(request.form.getlist('deposit_date_chk')): data['deposit_date']=[self.formValue('deposit_date_start'), self.formValue('deposit_date_end')]
        if bool(request.form.getlist('cust_name_chk')): data['cust_name'] = self.formValue('cust_name')
        if bool(request.form.getlist('req_date_chk')): data['req_date'] = [self.formValue('req_date_start'), self.formValue('req_date_end')]
        if bool(request.form.getlist('bank_req_date_chk')): data['bank_req_date'] = [self.formValue('bank_req_date_start'), self.formValue('bank_req_date_end')]
        if bool(request.form.getlist('status_chk')): data['status'] = [self.formValue('status')]

        # Job Status Colour Assignment
        color_chk = {}
        color_chk['已請款'] = 'blue'
        color_chk['未請款'] = 'orange'
        color_chk['作廢'] = 'pink'
        color_chk['退款'] = 'yellow'

        try:
            results = DBoperator(MailOrder).dyn_filter_query(self.data)
            # print ("查詢結果", results)
            index = 0
            query_dict = {}
            for r in results:
                query_dict.update({index: {
                    "status": r.status,
                    "order_id": r.order_id,
                    "store_name": r.store_name,
                    "r_id": r.r_id,
                    "r_name": r.r_name,
                    "auth_code": r.auth_code,
                    "auth_date": str(r.auth_date),
                    "req_date": str(r.req_date),
                    "bank_req_date": str(r.bank_req_date),
                    "card_holder": r.card_holder,
                    "cust_name": r.cust_name,
                    "cust_id": r.cust_id,
                    "card_num": r.card_num,
                    "bank": r.bank,
                    "card_exp": r.card_exp,
                    "payway": r.payway,
                    "amount": r.amount,
                    "last3": r.last3,
                    "mod_date": str(r.mod_date),
                    "mod_r_id": r.mod_r_id,
                    "signature": r.signature
            }})
                index += 1
            # print(query_dict)
            return query_dict, 200
        except Exception as e:
            print(e)
            return str(e), 401

    def update_daily(self, data):
        try:
            for row in data:
                try:
                    row['mod_id'] = current_user.id
                    row['mod_date'] = datetime.now().strftime("%Y%m%d%H%M%S")
                    result=DBoperator(DailyRPT).merge(row)
                    print(result)
                except Exception as e:
                    return (jsonify("有資料錯誤，請重新確認"), 400)
            return (jsonify("資料更新成功"), 200)


        except Exception as e:
            print(e)
            return str(e), 401

    def update_cashPymt(self, data):
        try:
            for row in data:
                try:
                    row['mod_id'] = current_user.id
                    row['mod_date'] = datetime.now().strftime("%Y%m%d%H%M%S")
                    result=DBoperator(DailyRPT).merge(row)
                    print(result)
                except Exception as e:
                    return (jsonify("有資料錯誤，請重新確認"), 400)
            return (jsonify("資料更新成功"), 200)

        except Exception as e:
            print(e)
            return (jsonify(e))

    # def update_mailOrder(self, data):
    #     try:
    #         for row in data:
    #             row_new ={}
    #             row_new['order_id'] = row ['order_id']
    #             row_new['status'] = row['status']
    #             row_new['auth_code'] = row ['auth_code']
    #             row_new['auth_date'] = None if row ['auth_date'] == "None" else row ['auth_date']
    #             row_new['req_date'] = None if row ['req_date'] == "None" else row ['req_date']
    #             row_new['bank_req_date'] = None if row ['bank_req_date'] == "None" else row ['bank_req_date']
    #             row_new['mod_date'] = datetime.now().strftime("%Y%m%d%H%M%S")
    #             row_new['mod_r_id'] = current_user.id
    #
    #             result=DBoperator(MailOrder_updated).merge(row_new)
    #             print(result)
    #             (jsonify("資料更新成功"), 200)
    #     except Exception as e:
    #         print("查詢錯誤: ", e)
    #         return (jsonify(e), 400)

    def update_mailOrder(self):
        try:
            row_new = {}
            for r in self.data["data"]:
                for key, value in r.items():
                    print(key, value)
                    if value == "null" or value == "Null" or value == "None":value = None
                    if key == "status":row_new["status"] = value
                    if key == "order_id":row_new["order_id"] = value
                    if key == "store_id":row_new["store_id"] = value
                    if key == "store_name":row_new["store_name"] = value
                    if key == "r_id":row_new["r_id"] = value
                    if key == "r_name":row_new["r_name"] = value
                    if key == "auth_code":row_new["auth_code"] = value
                    if key == "auth_date":row_new["auth_date"] = value
                    if key == "req_date":row_new["req_date"] = value
                    if key == "bank_req_date":row_new["bank_req_date"] = value
                    if key == "card_holder":row_new["card_holder"] = value
                    if key == "cust_name":row_new["cust_name"] = value
                    if key == "cust_id":row_new["cust_id"] = value
                    if key == "card_num":row_new["card_num"] = value
                    if key == "bank":row_new["bank"] = value
                    if key == "card_exp":row_new["card_exp"] = value
                    if key == "payway":row_new["payway"] = value
                    if key == "amount":row_new["amount"] = value
                    if key == "last3" and value is not None:row_new["last3"] = int(value)
                    if key == "mod_date":row_new["mod_date"] = value
                    if key == "mod_r_id":row_new["mod_r_id"] = value
                print("資料更新成功")
                print(row_new)
                DBoperator(MailOrder_updated).merge(row_new)
            return "資料更新成功", 200
        except Exception as e:
            print("更新錯誤: ", e)
            return (jsonify(e), 400)

    def delete(self, id, tab):
        data = {}
        try:
            if tab == 'daily':
                print("處理每日必填")
                data['item_num'] = id
                result=DBoperator(DailyRPT).delete(data)
                return result
            elif tab == 'cashPymtSearch':
                print("處理現金匯款單")
                data['cashpymt_id'] = id
                print (id)
                result=DBoperator(CashPymt).delete(data)
                return result
            elif tab == 'cashPymt':
                print("處理現金匯款單")
                data['pymt_order_seq'] = id
                print (id)
                result=DBoperator(CashPymt).delete(data)
                return result
            elif tab == 'mailOrder':
                result=DBoperator(MailOrder).delete(data)
                return result
        except Exception as e:
            print("查詢錯誤: ", e)
            return str(e)

    def excel_query(self):
        print("excel_query")

    # def write_csv(self):
    #     try:
    #         headers = self.data["data"][0].keys()
    #         si = StringIO()
    #         cw = csv.writer(si)
    #         cw.writerow(headers)
    #         csv_list = []
    #         for r in self.data["data"]:
    #             for key, value in r.items():
    #                 csv_list.append(value)
    #         cw.writerow(csv_list)
    #         response = make_response(si.getvalue())
    #         response.headers['Content-Disposition'] = 'attachment; filename = export.csv'
    #         response.headers['Content-type'] = 'text/csv'
    #         return response, 200
    #     except Exception as e:
    #         print(e)
    #         return "error", 411
    def write_csv(self):
        print("write_csv")
        path ="C:\\Users\\roy0001919\\Desktop\\export.xlsx"
        load_path = "C:\\Users\\roy0001919\\Desktop\\export.xlsx"
        # path = "/app/export.csv"
        # load_path = "/app/export.csv"

        if os.path.exists(path):
            try:
                os.remove(path)
                print("已經刪除之前的輸出檔案")
            except Exception as error:
                print ("刪除失敗: " + error)
                raise
        try:
            headers = self.data["data"][0].keys()
            print(headers)
            print("CSV標題:", headers)
            with open(load_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                for r in self.data["data"]:
                    print(r)
                    writer.writerow(r)
            # return (jsonify('資料匯出完成'), 200)
            #
            # results = {'status':'delete','success':'success', 'path': path2}
            print("資料匯出完成")

            return load_path, 200
        except Exception as e:
            print(e)
            return str(e), 401

    def return_url(self):
        return
    def responseCSV(self, loadpath):
        with open(loadpath, newline='') as f:
            spamreader = csv.reader
    def insertdb(self, app):
        with app.app_context():
            print("insertdb")
            self.update_mailOrder()

    def save_csv(self, app, q):
        with app.app_context():
            # self.query_mailOrder()
            result = self.write_csv()
            q.put(result)
            # self.return_url()

    # def export_csv(self, app):
    #     with app.app_context():
    #         try:
    #             # insertdb = threading.Thread(target=self.insertdb, args=[app, bookingRecord])
    #             # save_csv = threading.Thread(target=self.save_csv, args=[app, smbody, phone])
    #             print(self.data)
    #             insertdb = threading.Thread(target=self.insertdb, args=[app])
    #             save_csv = threading.Thread(target=self.save_csv, args=[app])
    #             # Start the threads
    #             insertdb.start()
    #             save_csv.start()
    #             ready_file = make_response(
    #                 StringIO.getvalue()
    #             )
    #
    #             # self.query_mailOrder()
    #             # self.write_csv()
    #             # self.return_url()
    #
    #             # print current threads
    #             return jsonify(ready_file), 200
    #         except Exception as e:
    #             print(e)
    #             return str(e), 500

    def formValue(self, *arg):
        result=""
        for a in arg:
            elem = request.form.get(a)
            if elem :
                result += elem
            else:
                return None
        return result

    