import ast
import operator
import uuid
from functools import reduce

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from rest_framework.decorators import api_view

from history.models import Entry


def index(request):
    template = loader.get_template('fast/about.html')
    return HttpResponse(template.render({}, request))


@api_view(['GET'])
# @login_required(login_url='/auth/login')
def fast_operation(request, operation):
    template = loader.get_template('fast/operation.html')
    args_list = request.GET.getlist('args')
    r = Entry(id=uuid.uuid4(), user=request.user, operation_type=operation, operands=[0.0], result=[0.0])
    if len(args_list) != 0:
        args = list(map(float, ast.literal_eval(args_list[0])))
        r.operands = args
    else:
        return HttpResponseBadRequest("Not enough arguments '?args=[]'")
    if operation == 'sum':
        r.result = [reduce(operator.add, args)]
    elif operation == 'sub':
        r.result = [reduce(operator.sub, args)]
    elif operation == 'mul':
        r.result = [reduce(operator.mul, args)]
    elif operation == 'div':
        try:
            r.result = [reduce(operator.truediv, args)]
        except ZeroDivisionError:
            return HttpResponseBadRequest("An attempt to divide by zero has been stopped")
    else:
        return HttpResponseBadRequest("Incorrect operation type")
    r.save()
    return HttpResponse(template.render({'result': r}, request))
