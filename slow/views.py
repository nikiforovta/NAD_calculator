import ast
import math
import threading
import uuid
from time import sleep

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from rest_framework.decorators import api_view

from history.models import Entry


def index(request):
    template = loader.get_template('slow/about.html')
    return HttpResponse(template.render({}, request))


@api_view(["GET"])
@login_required(login_url='/auth/login')
def slow_operation(request, operation):
    template = loader.get_template('slow/operation.html')
    args_list = request.GET.getlist('args')
    r = Entry(id=uuid.uuid4(), user=request.user, operation_type=operation, operands=[0.0], result=[0.0])
    if len(args_list) != 0:
        args = list(map(float, ast.literal_eval(args_list[0])))
    else:
        return HttpResponseBadRequest("Not enough arguments '?args=[]'")
    if operation == 'sqrt':
        threading.Thread(target=slow_sqrt, kwargs={"operation_id": r.id, "args": args}).start()
    elif operation == 'fact':
        threading.Thread(target=slow_fact, kwargs={"operation_id": r.id, "args": args}).start()
    else:
        return HttpResponseBadRequest("Incorrect operation type")
    r.save()
    return HttpResponse(template.render({"result": r}, request))


def get_request(operation_id):
    while True:
        request = Entry.objects.filter(id=operation_id).first()
        if request:
            return request


def slow_sqrt(operation_id, args):
    sleep(len(args) * 2)
    request = get_request(operation_id)
    request.result = list(map(lambda x: x ** 0.5, args))
    request.save()


def slow_fact(operation_id, args):
    sleep(len(args) * 2)
    request = get_request(operation_id)
    try:
        request.result = list(map(lambda x: math.factorial(x), args))
    except ValueError:
        request.operation_type = "Fail"  # "An attempt to calculate the factorial for an unsuitable operand has been stopped"
    finally:
        request.save()
