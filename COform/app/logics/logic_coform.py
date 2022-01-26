#  -*- coding: UTF-8 -*-

from datetime import date, datetime
from ..dbmodels.dbOperator import DBoperator
from ..dbmodels.models import MailOrder
from datetime import datetime

class Logic_coform():
    def __init__(self, data):
        self.data = data
    
    def insert(self):
        coDict=self.chacker()
        conditions = self.conditions(**coDict)
        if conditions == True:
            message="資料輸入: "+str(coDict)
            print(message)
            print(coDict)
            return DBoperator(MailOrder).insert(coDict)
        else:
            return "資料有誤: "+conditions, 401

    def coform_search_open(self):
        print(self.data)
        results = DBoperator(MailOrder).dyn_filter_query(self.data)
        datetime_dt = datetime.today()
        mod_id = datetime_dt.strftime("%Y%m%d%H%M%S")
        index = 0
        # print(results.len())
        query_set = {}
        query_dict = {}
        for r in results:
            query_dict.update({index: {
                "order_id": r.order_id,
                "store_id": r.store_id,
                "cust_name": r.cust_name,
                "cust_id": r.cust_id,
                "amount": r.amount,
                "auth_code": r.auth_code
            }})
            index += 1
            query_set.update(
                {
                    "mod_id": r.store_id + "-" + mod_id,
                    "data": query_dict
                }
            )
        return query_set, 200
        # coDict = self.chacker()
        # conditions = self.conditions(**coDict)
        # if conditions == True:
        #     message = "資料輸入: " + str(coDict)
        #     print(message)
        #     print(coDict)
        #     return DBoperator(MailOrder).dyn_filter_query(coDict)
        # else:
        #     return "資料有誤: " + conditions, 401

    def modifyTracking(self):
        data = self.data
        data['r_id']
        
        coDict_store={}
        coDict_store['auth_code']=self.formValue('auth_code')
        coDict_store['auth_date']=self.formValue('auth_date')
        coDict_store['req_date']=self.formValue('req_date')
        coDict_store['mod_r_id']=self.formValue('r_id')

        #test if coDict_store contains NoneType
        if None not in coDict_store.values():
            message="資料輸入: "+str(coDict_store)
            print(message)
            sql = "UPDATE public.web_fin_mailorder SET auth_code={}, auth_date={}, req_date={}, mod_r_id={}, mod_date={}, r_id={}, r_name={}, bank_req_date={} WHERE coform_id={}".format(coDict_store['auth_code'],coDict_store['auth_date'],coDict_store['req_date'],coDict_store['mod_r_id'],coDict_store['mod_date'],coDict_store['r_id'],coDict_store['r_name'], coDict_store['bank_req_date'],coDict_store['coform_id'])
            return DBoperator(MailOrder).customSQL(sql)
            # return DBoperator(MailOrder_mods).insert(coDict_store)
        else:
            return "資料有誤: 請確認是否有空白值", 401

    def delete(self, id):
        data = {}
        data['order_id']=str(id)
        return DBoperator(MailOrder).delete(data)


    def chacker(self):
        coDict={}
        coDict['order_id'] = self.formValue('order_id') 
        coDict['store_id'] = self.formValue('store_id')
        coDict['store_name'] = self.formValue('store_name')
        coDict['r_id'] = self.formValue('r_id')
        coDict['r_name'] = self.formValue('r_name')
        coDict['cust_name']= self.formValue('cust_name') #not none
        coDict['cust_id']= self.formValue('cust_id') #not none
        coDict['payway']= self.formValue('payway')
        coDict['auth_code'] = self.formValue('auth_code')
        coDict['auth_date'] = self.formValue('auth_date')
        coDict['req_date'] = self.formValue('req_date')
        coDict['card_holder'] = self.formValue('card_holder')
        coDict['bank'] = self.formValue('bank')
        coDict['card_num'] = self.formValue('card_num')
        # if self.formValue('last3') and len(self.formValue('last3')) == 3:
        #     coDict['last3'] = self.formValue('last3')
        coDict['last3'] = self.formValue('last3')
        coDict['card_exp'] = self.formValue('card_exp')
        coDict['amount'] = self.formValue('amount')
        coDict['signature'] = self.formValue('signature')
        coDict['status'] = '未請款'

        for i in coDict:
            print(i,':',coDict[i],type(coDict[i]))        

        return coDict
    def formValue(self, *arg):
        result=""
        for a in arg:
            elem = self.data[a]
            if elem :
                result += elem
            else:
                return None
        return result



    def conditions (self, **coDict):
        condition={}
        condition['authCode'] = True if (self.formValue('payway') == 'pay_later') else(
                            True if not(
                                (coDict['auth_code'] is None) or 
                                (coDict['auth_date'] is None or coDict['req_date'] is None)
                            )   else '請確認授權碼、授權日期、請款日期欄位'
                        )

        condition['card_num'] = True if (coDict['card_num'] is not None and len(coDict['card_num']) ==16) else False


        # condition['last3'] = True if (
        #                         (coDict['last3'] is not None) and
        #                         (len(coDict['last3'])==3 )
        #                     )else '請輸入卡片後三碼'
        if coDict['last3'] is not None and (len(coDict['last3']) == 3) or coDict['last3'] is None:
            condition['last3'] = True
        elif coDict['last3'] is not None and (len(coDict['last3'])<3 ) and (len(coDict['last3'])>0 ):
            condition['last3'] = '卡片後三碼輸入不完整'
        else:
            condition['last3'] = '卡片後三碼輸入錯誤'
        condition['cust_name'] = True if coDict['cust_name'] is not None else '請輸入會員姓名'
        condition['cust_id'] = True if coDict['cust_id'] is not None else '請輸入會員ID'
        condition['bank'] = True if coDict['bank'] != '請選擇' else '請選擇銀行'
        # condition['card_exp'] = True if coDict['card_exp'] is not None else '信用卡有效期限'
        if coDict['card_exp'] is not None and len(coDict['card_exp']) == 7 and int(coDict['card_exp'][0:2]) <= 12 and int(coDict['card_exp'][3:7]) <= 2099:
            condition['card_exp'] = True
        else:
            condition['card_exp'] = '信用卡有效期限錯誤'
        condition['signature'] = True if coDict['signature'] is not None else '請簽名'

        for key,value in condition.items():
            if value != True:
                print ('error in '+key+' : '+value)
                return value
        
        return True

