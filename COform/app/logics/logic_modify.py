from ..dbmodels.dbOperator import DBoperator
from ..dbmodels.models import MailOrder_mods, MailOrder

class Logic_Mod:
    def __init__(self, data):
        self.data = data
    
    def insert_COform(self):
        modDict = {}
        if self.formValue('mod_id'):
            modDict['mod_id'] = self.formValue('mod_id')[0:-3]
            modDict['mod_id_seq'] = self.formValue('mod_id')
            print(modDict['mod_id'])
            print(modDict['mod_id_seq'])
        if self.formValue('coform_id'):
            modDict['coform_id'] = self.formValue('coform_id')
        # if self.formValue('status'):
        modDict['status'] = "未請款"
        if self.formValue('auth_code'):
            modDict['auth_code'] = self.formValue('auth_code')
        if self.formValue('auth_date'):
            modDict['auth_date'] = self.formValue('auth_date')
        if self.formValue('req_date'):
            modDict['req_date'] = self.formValue('req_date')
        if self.formValue('bank_req_date'):
            modDict['bank_req_date'] = self.formValue('bank_req_date')
        if self.formValue('mod_r_id'):
            modDict['mod_r_id'] = self.formValue('mod_r_id')
        if self.formValue('mod_date'):
            modDict['mod_date'] = self.formValue('mod_date')
        #test if modDict contains NoneType
        for key, value in modDict.items():
            if key != 'bank_req_date' and value is None:
                return '資料填寫不全，請重新確認', 403
        sql = "UPDATE public.web_fin_mailorder SET auth_code='{}', auth_date='{}', req_date='{}', mod_r_id='{}', mod_date='{}', bank_req_date='{}' WHERE order_id='{}'".format(modDict['auth_code'], modDict['auth_date'], modDict['req_date'], modDict['mod_r_id'], modDict['mod_date'], modDict['bank_req_date'], modDict['coform_id'])
        return DBoperator(MailOrder).customSQL(sql)
        # return DBoperator(MailOrder_mods).insert(modDict)

    def formValue(self, *arg):
        result=""
        for a in arg:
            elem = self.data[a]
            if elem:
                result += elem
                # print(result)
            else:
                # print('formValue returns none')
                return None
        return result