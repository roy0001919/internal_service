#  -*- coding: UTF-8 -*-

from . import models_bp,db 
from .models import DailyRPT
from sqlalchemy.exc import IntegrityError
from datetime import datetime
class DBoperator:
    def __init__(self, table):
        self.table = table

# ''' Inserting Data '''
    def insert(self, data):
        insert_data = self.table(**data)
        try:
            db.session.add(insert_data)
            db.session.commit()
            return "資料寫入成功:", 200
            # return "資料寫入成功: "+insert_data.order_id, 200
        except Exception as e:
            db.session.rollback()
            print(e)
            return str(e), 401

# ''' Updating Data if exist, Insert in not exist '''
    def merge(self, data):

        merge_data = self.table(**data)
        try:
            db.session.merge(merge_data)
            # db.session.insert(self.table_log(**data))
            db.session.commit()
            return "資料更新成功: ", 200
        except IntegrityError as e:
            db.session.rollback()
            print(str(e))
            return str(e), 401

# ''' Deleting Data '''
    def delete(self, data):
        # delete_data = self.table.query.filter_by(item_num = id).first()
        # db.session.delete(delete_data)
        # db.session.commit()
        print("準備刪除")
        try:
            qry = self.table.query
            for attr, value in data.items():
                print(attr, value)
                qry = qry.filter( getattr(self.table, attr) == value).first()
            print("qry: ",qry)
            db.session.delete(qry)
            db.session.commit()
            print("刪除成功")
            return "資料刪除成功", 200
        except IntegrityError as e:
            db.session.rollback()
            print(str(e))
            return str(e), 401

    
    def retrieve(self,data):
        try:
            records = self.table.query.filter_by(store_id = data).order_by(self.table.datetimestamp.desc()).limit(10)
            db.session.commit()
            return records, 200
        except Exception as e:
            print(e)
            return str(e), 401

# ''' Search Query by date range and store '''

    def dateRange_query(self,data):
        print("執行dateRange_query")
        try:
            qry = self.table.query.filter(self.table.data_src_date.between(data['date_start'],data['date_end'])).\
                                filter_by(store_id =data['store'],pymt_method=data['pymt_method']).limit(100).all()
            print(qry)
            return qry, 200
        except IntegrityError as e:
            print (str(e))
            return str(e), 401


    def dyn_filter_query(self, data):
        print("執行dyn_filter_query")
        # qry = self.table.query.filter(self.table.req_date.between(data['date_start'],data['date_end']))
        print(type(self.table))
        try:
            qry = self.table.query
            for attr, value in data.items():
                print(attr, value)
                if "req_date" in attr or "r_date" in attr or "bank_req_date" in attr or "auth_date" in attr or "dep_date" in attr or "deposit_date" in attr or "pymt_date" in attr:
                    qry = qry.filter(getattr(self.table, attr).between(value[0], value[1]))
                elif "data_src_date" in attr:
                    try:
                        datetime.strptime(value, "%Y-%m-%d")
                        qry = qry.filter(getattr(self.table, attr) == value)
                    except:
                        qry = qry.filter(getattr(self.table, attr).between(value[0], value[1]))
                else:
                    qry = qry.filter(getattr(self.table, attr) == value)
            results = qry.limit(100).all()
            db.session.commit()
            # print(results)
            return results
        except IntegrityError as e:
            db.session.rollback()
            print(str(e))
            return str(e), 401

    def auth_user_query(self, data):
        print("執行auth_user_query")
        # qry = self.table.query.filter(self.table.req_date.between(data['date_start'],data['date_end']))
        print(type(self.table))
        try:
            qry = self.table.query
            for attr, value in data.items():
                print(attr, value)
                qry = qry.filter(getattr(self.table, attr) == value)
            # results = qry.limit(300).all()
            db.session.commit()
            # print(results)
            return qry
        except IntegrityError as e:
            db.session.rollback()
            print(str(e))
            return str(e), 401
            #     else:
            #         qry = qry.filter(getattr(self.table, attr) == value)
            #         results = qry.all()
            #         db.session.commit()
            #         print(results)
            #     if "pymt_method" in attr:
            #         print("付款方式: ", value)
            #         qry = qry.filter(db.or_(*(getattr(self.table, attr) == s for i, s in enumerate(value))))
            #     elif "date" in attr or "cnt" in attr:
            #         print("搜尋Date Range")
            #         qry = qry.filter( getattr(self.table, attr).between(value[0],value[1]))
            #     else:
            #         print("執行其他query")
            #         qry = qry.filter( getattr(self.table, attr) == value)
            # results = qry.all()
            # db.session.commit()
            # return results, 200


    def customSQL(self, sql):
        try:
            exe = db.engine.execute(sql)
            db.session.commit()
            msg = ('客製化SQL執行成功. ')
            return msg
        except IntegrityError as e:
            msg = ('客製化SQA執行失敗: ', str(e), ' ,')
            return msg, 401

        