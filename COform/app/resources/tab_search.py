from flask import request, current_app, make_response, Response
from flask_restful import Resource
from ..logics.logic_search import Logic_search
import threading, queue
from io import StringIO
import csv
import json

class SearchCashPymt(Resource):

    def post(self):
        data = request.json
        result = Logic_search(data).query_cashPymt()
        return result


class SearchCashDelete(Resource):

    def delete(self, id, tab):
        data = request.json
        result = Logic_search(data).delete(id, tab)
        return result


class SearchMailOrder(Resource):

    def post(self):
        data = request.json
        result = Logic_search(data).query_mailOrder()
        return result


class SearchMailOrderUpdate(Resource):

    def post(self):
        data = request.json
        result = Logic_search(data).update_mailOrder()
        return result


class ExportCsv(Resource):

    def post(self):
        data = request.json
        q = queue.Queue()
        # to introduct app from higher level, use
        # current_app object from flask and implement the
        # _get_current_object function
        app = current_app._get_current_object()
        # result = Logic_search(data).export_csv(app)
        insertdb = threading.Thread(target=Logic_search(data).insertdb, args=[app])
        save_csv = threading.Thread(target=Logic_search(data).save_csv, args=[app, q])
        # insertdb.start()
        save_csv.start()
        queue_value = q.get()
        print('\n\n\n\n\n\n\n'+str(queue_value)+'\n\n\n\n\n\n\n')
        print(data)
        # csv = """"REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"
        # "1985/01/21","Douglas Adams",0345391802,5.95
        # "1990/01/12","Douglas Hofstadter",0465026567,9.95
        # "1998/07/15","Timothy ""The Parser"" Campbell",0968411304,18.99
        # "1999/12/03","Richard Friedman",0060630353,5.95
        # "2004/10/04","Randel Helms",0879755725,4.50"""
        # response = make_response(csv)
        headers = data["data"][0].keys()
        print(headers)
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(headers)
        csv_list = []
        for r in data["data"]:
            # cw.writerow(r)
            for key, value in r.items():
                csv_list.append(value)
                print(value)
        print(csv_list)
        cw.writerow(csv_list)
        # response = make_response(si.getvalue())
        # response.headers['Content-Disposition'] = 'attachment; filename = export.csv'
        # response.headers['Content-Type'] = 'text/csv'
        # print(response)
        # return response
        return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=export.csv"})
