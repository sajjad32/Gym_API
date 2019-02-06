import json
from .jalali import *

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from .models import *


def index(request):
    users = User.objects.all().values()
    return JsonResponse({'users': list(users)})

def show(request, id):
    user = User.objects.filter(id=id).values()
    presents = Present.objects.filter(user_id=id).values()
    payments = Payment.objects.filter(user_id=id).values()
    # return JsonResponse({'user': list(user), 'presents': list(presents), 'payments': list(payments)})
    return JsonResponse({'user': list(user), 'presents': list(presents), 'payments': list(payments)})


@method_decorator(csrf_exempt)
def add(request):
    if(request.method == 'POST'):
        req = json.loads(request.body)['user']
        new_user = User(name=req['name'], phoneNo=req['phoneNo'], shelfNo=req['shelfNo'], details=req['details'])
        new_user.save()
        return JsonResponse({'status': 200, 'message': 'user added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def update(request, id):
    if(request.method == 'POST'):
        req = json.loads(request.body)['user']
        user = User.objects.filter(id=id).values()
        user.update(name=req['name'], phoneNo=req['phoneNo'], shelfNo=req['shelfNo'], details=req['details'])
        return JsonResponse({'status': 200, 'message': 'user updated successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def delete(request, id):
    if(request.method == 'DELETE'):
        user = User.objects.filter(id=id)
        user.delete()
        return JsonResponse({'status': 200, 'message': 'user deleted successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


def todayPresence(request):
    if(request.method == 'GET'):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        presents = Present.objects.filter(date=today).select_related('user').values('user__name', 'enterTime', 'outTime')
        return JsonResponse({'presents': list(presents)})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def addEnter(request, id):
    if(request.method == 'POST'):
        req = json.loads(request.body)['present']
        new_present = Present(user_id=id, enterTime=req['enterTime'], date=req['date'])
        new_present.save()
        User.objects.filter(id=id).update(flag=True)
        return JsonResponse({'status': 200, 'message': 'presence added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def addOut(request, id):
    if (request.method == 'POST'):
        present = Present.objects.filter(user_id=id, outTime__isnull=True)
        req = json.loads(request.body)['absence']
        present.update(outTime=req['outTime'])
        User.objects.filter(id=id).update(flag=False)
        return JsonResponse({'status': 200, 'message': 'absence added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


def paymentList(request):
    if(request.method == 'GET'):
        payments = Payment.objects.select_related('user').values('user__name', 'date', 'price', 'method')
        return JsonResponse({'payments': list(payments)})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def addPayment(request, id):
    if(request.method == 'POST'):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        req = json.loads(request.body)['payment']
        new_payment = Payment(price=req['price'], method=req['method'], date=today, user_id=id)
        new_payment.save()
        return JsonResponse({'status': 200, 'message': 'payment added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def userDiagram(request):
    if(request.method == 'POST'):
        req = json.loads(request.body)['data']
        startDate = Persian(req['startDate']).gregorian_string()
        endDate = Persian(req['endDate']).gregorian_string()
        usersNo = []
        res = Present.objects.raw("SELECT T.id AS id, T.date AS date, CO FROM (SELECT id, date, COUNT(date) as CO FROM `user_present` GROUP BY date ) as T WHERE (T.date >= %s AND T.date <= %s)", [startDate, endDate])
        for record in res:
            date = Gregorian(record.date).persian_string()
            usersNo.append({'date': date, 'count': record.CO})
        return JsonResponse({'usersNo': list(usersNo)})
    return JsonResponse({'status': 500, 'message': 'request method error'})