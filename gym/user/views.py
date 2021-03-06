import json
import time

from .jalali import *

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import *


@method_decorator(csrf_exempt)
def index(request):
    if (request.method == 'POST'):
        req = json.loads(request.body)['users_id']
        users = User.objects.all().values()
        users = users.order_by('-registerDate')[req['startIndex']:(req['startIndex'] + req['recordsPerPage'])]
        array_length = users.count()
        return JsonResponse({'users': list(users), 'count': array_length})
    return JsonResponse({'status': 500, 'message': 'request method error'})


def search(request):
    users = User.objects.all().values()
    return JsonResponse({'users': list(users)})


def show(request, id):
    user = User.objects.filter(id=id).values()
    presents = Present.objects.filter(user_id=id).values()
    payments = Payment.objects.filter(user_id=id).values()
    exercises = Exercise.objects.filter(user_id=id).values()
    return JsonResponse({'user': list(user), 'presents': list(presents), 'payments': list(payments), 'exercises': list(exercises)})


@method_decorator(csrf_exempt)
def add(request):
    if(request.method == 'POST'):
        g_today = datetime.datetime.now().strftime("%Y-%m-%d")
        p_today = Gregorian(g_today).persian_string()
        req = json.loads(request.body)['user']
        new_user = User(name=req['name'], phoneNo=req['phoneNo'], shelfNo=req['shelfNo'], details=req['details'], registerDate=p_today)
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


@method_decorator(csrf_exempt)
def todayPresence(request):
    if(request.method == 'POST'):
        g_today = datetime.datetime.now().strftime("%Y-%m-%d")
        p_today = Gregorian(g_today).persian_string()
        req = json.loads(request.body)['today']
        presents = Present.objects.filter(date=p_today).select_related('user').values('user__name', 'enterTime', 'outTime')
        array_length = presents.count()
        presents = presents.order_by('-enterTime')[req['startIndex']:(req['startIndex']+req['recordsPerPage'])]
        return JsonResponse({'presents': list(presents), 'count': array_length})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def addEnter(request, id):
    if(request.method == 'POST'):
        g_today = datetime.datetime.now().strftime("%Y-%m-%d")
        p_today = Gregorian(g_today).persian_string()
        req = json.loads(request.body)['present']
        new_present = Present(user_id=id, enterTime=req['enterTime'], date=p_today)
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


@method_decorator(csrf_exempt)
def paymentList(request):
    if(request.method == 'POST'):
        req = json.loads(request.body)['req_month']
        payments = Payment.objects.filter(date__range=[req['start_month'], req['end_month']]).select_related('user').values('user__name', 'date', 'price', 'method')
        return JsonResponse({'payments': list(payments)})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def addPayment(request, id):
    if(request.method == 'POST'):
        g_today = datetime.datetime.now().strftime("%Y-%m-%d")
        p_today = Gregorian(g_today).persian_string()
        req = json.loads(request.body)['payment']
        new_payment = Payment(price=req['price'], method=req['method'], date=p_today, user_id=id)
        new_payment.save()
        return JsonResponse({'status': 200, 'message': 'payment added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def addExercise(request):
    if(request.method == 'POST'):
        g_today = datetime.datetime.now().strftime("%Y-%m-%d")
        p_today = Gregorian(g_today).persian_string()
        req = json.loads(request.body)['exercise']
        new_exercise = Exercise(details=req['detail'], user_id=req['user_id'], date=p_today)
        new_exercise.save()
        return JsonResponse({'status': 200, 'message': 'exercise added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def updateExercise(request):
    pass


@method_decorator(csrf_exempt)
def userDiagram(request):
    if(request.method == 'POST'):
        req = json.loads(request.body)['data']
        startDate = req['startDate']
        endDate = req['endDate']
        usersNo = []
        res = Present.objects.raw("SELECT T.id AS id, T.date AS date, CO FROM (SELECT id, date, COUNT(date) as CO FROM `user_present` GROUP BY date ) as T WHERE (T.date >= %s AND T.date <= %s)", [startDate, endDate])
        for record in res:
            usersNo.append({'date': record.date, 'count': record.CO})
        return JsonResponse({'usersNo': list(usersNo)})
    return JsonResponse({'status': 500, 'message': 'request method error'})


@method_decorator(csrf_exempt)
def uploadUserImage(request):
    if (request.method == 'POST'):
        req = json.loads(request.body)['data']
        user = User.objects.filter(id=req['user_id']).values()
        user.update(image=req['image'])
        return JsonResponse({'status': 200, 'message': 'image added successfully'})
    return JsonResponse({'status': 500, 'message': 'request method error'})


def setUsersOut():
    time.sleep(10)
    print("this  function ran after 10 seconds")