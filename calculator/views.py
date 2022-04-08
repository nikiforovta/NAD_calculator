from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CalculatorForm


def index(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            arguments = form.cleaned_data['arguments']
            operation_type = form.cleaned_data['operation_type']
            speed = 'slow' if len(operation_type) == 4 else 'fast'
            arguments = [float(argument) for argument in arguments.split('\r\n')]
            return HttpResponseRedirect(
                f'/api/{speed}/{operation_type}?args={arguments}')
        else:
            form = CalculatorForm(initial={'operation_type': form.cleaned_data['operation_type'], 'arguments': 'Incorrect operands'})
    else:
        operation_type = request.GET.get('type')
        form = CalculatorForm(initial={'operation_type': operation_type})
    return render(request, 'calculator/calculator.html', {'form': form})
