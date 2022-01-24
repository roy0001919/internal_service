from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")


@login_required
def tab_coform(request):

    datetime_dt = datetime.today()  # 獲得當地時間
    order_id = datetime_dt.strftime("%Y%m%d%H%M%S")  # 格式化日期

    return render(
        request,
        'myweb/tab_coform.html',
        {"order_id": order_id},
    )

@login_required
def tab_daily(request):

    datetime_dt = datetime.today()  # 獲得當地時間
    item_num = datetime_dt.strftime("%Y%m%d%H%M%S")  # 格式化日期

    return render(
        request,
        'myweb/tab_daily.html',
        {"item_num": item_num},
    )

@login_required
def tab_cashpymt(request):

    datetime_dt = datetime.today()  # 獲得當地時間
    cashPymt_id = datetime_dt.strftime("%Y%m%d%H%M%S")  # 格式化日期

    return render(
        request,
        'myweb/tab_cashpymt.html',
        {"cashPymt_id": cashPymt_id},
    )

@login_required
def tab_search(request):

    return render(
        request,
        'myweb/tab_search.html',
        {},
    )

@login_required
def index(request):
    return render(
        request,
        'myweb/base.html',
        {},
    )

@login_required
def daily(request):
    if request.method == 'POST':
        checked_dict = {}
        print(request.POST)
        if "selection1" in request.POST:
            store_name = request.POST['store_name']
            if isinstance(store_name, str) and len(store_name) == 2:
                print(store_name)
                checked_dict.update({"store_name": request.POST['store_name']})
        if "selection2" in request.POST:
            r_id = request.POST['r_id']
            if isinstance(r_id, str) and len(r_id) == 6:
                if r_id[0] == "s" or "S":
                    print(r_id)
                    checked_dict.update({"r_id": request.POST['r_id']})
        if "selection3" in request.POST:
            r_date_from = request.POST['r_date_from']
            try:
                r_date_from_check = datetime.strptime(r_date_from, "%Y-%m-%d")
                if str(r_date_from) == str(r_date_from_check.date()):
                    print(r_date_from_check.date())
                    checked_dict.update({"r_date_from": r_date_from})
            except:
                print("no datetime")
            r_date_to = request.POST['r_date_to']
            try:
                r_date_to_check = datetime.strptime(r_date_to, "%Y-%m-%d")
                if str(r_date_to) == str(r_date_to_check.date()):
                    print(r_date_to_check.date())
                    checked_dict.update({"r_date_to": r_date_to})
            except:
                print("no datetime")
        print(checked_dict)
    return render(
        request,
        'myweb/daily.html',
        {},
    )

@login_required
def mailOrder(request):
    if request.method == 'POST':
        checked_dict = {}
        print(request.POST)
        if "selection1" in request.POST:
            store_name = request.POST['store_name']
            if isinstance(store_name, str) and len(store_name) == 2:
                print(store_name)
                checked_dict.update({"store_name": request.POST['store_name']})
        if "selection2" in request.POST:
            status = request.POST['status']
            if status in ["已請款", "未請款", "作廢", "退款"]:
                print(status)
                checked_dict.update({"status": request.POST['status']})
        if "selection3" in request.POST:
            bank_req_date_from = request.POST['bank_req_date_from']
            try:
                bank_req_date_from_check = datetime.strptime(bank_req_date_from, "%Y-%m-%d")
                if str(bank_req_date_from) == str(bank_req_date_from_check.date()):
                    print(bank_req_date_from_check.date())
                    checked_dict.update({"bank_req_date_from": bank_req_date_from})
            except:
                print("no datetime")
            bank_req_date_to = request.POST['bank_req_date_to']
            try:
                bank_req_date_to_check = datetime.strptime(bank_req_date_to, "%Y-%m-%d")
                if str(bank_req_date_to) == str(bank_req_date_to_check.date()):
                    print(bank_req_date_to_check.date())
                    checked_dict.update({"bank_req_date_to": bank_req_date_to})
            except:
                print("no datetime")
        if "selection4" in request.POST:
            auth_date_from = request.POST['auth_date_from']
            try:
                auth_date_from_check = datetime.strptime(auth_date_from, "%Y-%m-%d")
                if str(auth_date_from) == str(auth_date_from_check.date()):
                    print(auth_date_from_check.date())
                    checked_dict.update({"auth_date_from": auth_date_from})
            except:
                print("no datetime")
            auth_date_to = request.POST['auth_date_to']
            try:
                auth_date_to_check = datetime.strptime(auth_date_to, "%Y-%m-%d")
                if str(auth_date_to) == str(auth_date_to_check.date()):
                    print(auth_date_to_check.date())
                    checked_dict.update({"auth_date_to": auth_date_to})
            except:
                print("no datetime")
        if "selection5" in request.POST:
            req_date_from = request.POST['req_date_from']
            try:
                req_date_from_check = datetime.strptime(req_date_from, "%Y-%m-%d")
                if str(req_date_from) == str(req_date_from_check.date()):
                    print(req_date_from_check.date())
                    checked_dict.update({"req_date_from": req_date_from})
            except:
                print("no datetime")
            req_date_to = request.POST['req_date_to']
            try:
                req_date_to_check = datetime.strptime(req_date_to, "%Y-%m-%d")
                if str(req_date_to) == str(req_date_to_check.date()):
                    print(req_date_to_check.date())
                    checked_dict.update({"req_date_to": req_date_to})
            except:
                print("no datetime")
        if "selection6" in request.POST:
            cust_name = request.POST['cust_name']
            if isinstance(cust_name, str) and int(len(cust_name)) <= 20:
                print(cust_name)
                checked_dict.update({"cust_name": cust_name})
        print(checked_dict)
    if request.user.is_superuser:
        return render(
            request,
            'myweb/mailOrder.html',
            {},
        )

@login_required
def cashPymt(request):
    if request.method == 'POST':
        checked_dict = {}
        print(request.POST)
        if "selection1" in request.POST:
            store_name = request.POST['store_name']
            if isinstance(store_name, str) and len(store_name) == 2:
                print(store_name)
                checked_dict.update({"store_name": request.POST['store_name']})
        if "selection2" in request.POST:
            deposit_date_from = request.POST['deposit_date_from']
            try:
                deposit_date_from_check = datetime.strptime(deposit_date_from, "%Y-%m-%d")
                if str(deposit_date_from) == str(deposit_date_from_check.date()):
                    print(deposit_date_from_check.date())
                    checked_dict.update({"deposit_date_from": deposit_date_from})
            except:
                print("no datetime")
            deposit_date_to = request.POST['deposit_date_to']
            try:
                deposit_date_to_check = datetime.strptime(deposit_date_to, "%Y-%m-%d")
                if str(deposit_date_to) == str(deposit_date_to_check.date()):
                    print(deposit_date_to_check.date())
                    checked_dict.update({"deposit_date_to": deposit_date_to})
            except:
                print("no datetime")
        if "selection3" in request.POST:
            date_src_date_from = request.POST['date_src_date_from']
            try:
                date_src_date_check = datetime.strptime(date_src_date_from, "%Y-%m-%d")
                if str(date_src_date_from) == str(date_src_date_check.date()):
                    print(date_src_date_check.date())
                    checked_dict.update({"date_src_date_from": date_src_date_from})
            except:
                print("no datetime")
            date_src_date_to = request.POST['date_src_date_to']
            try:
                date_src_date_to_check = datetime.strptime(date_src_date_to, "%Y-%m-%d")
                if str(date_src_date_to) == str(date_src_date_to_check.date()):
                    print(date_src_date_to_check.date())
                    checked_dict.update({"date_src_date_to": date_src_date_to})
            except:
                print("no datetime")
        if "selection4" in request.POST:
            cust_name = request.POST['cust_name']
            if isinstance(cust_name, str) and int(len(cust_name)) <= 20:
                print(cust_name)
                checked_dict.update({"cust_name": cust_name})
        print(checked_dict)

    return render(
        request,
        'myweb/cashPymt.html',
        {},
    )


def sched_createuser():
    url = "http://18.183.236.5/api/authuser"
    data = {"jobstatus": "正式"}
    request = requests.post(url, json=data)
    result = (request.json())
    for key, value in result.items():
        for k, v in value.items():
            if k == "id":
                try:
                    User.objects.get(username=v)
                except:
                    print(v)
                    user = User.objects.create_user(v, v + '@moz.com', v)
                    user.first_name = v
                    user.last_name = value["username"]
                    user.is_staff = "1"
                    if value["depart_name"] == "財務部":
                        user.is_superuser = "1"
                    user.save()


def sched_removeuser():
    url = "http://18.183.236.5/api/authuser"
    data = {"jobstatus": "離職"}
    request = requests.post(url, json=data)
    result = (request.json())
    for key, value in result.items():
        for k, v in value.items():
            if k == "id":
                print(v)
                try:
                    r = User.objects.get(username=v)
                    r.delete()
                except:
                    pass

scheduler.add_job(
    sched_createuser,
    'cron',
    hour=6,
    minute=00,
    max_instances=2
)
scheduler.add_job(
    sched_removeuser,
    'cron',
    hour=6,
    minute=00,
    max_instances=2
)

scheduler.start()