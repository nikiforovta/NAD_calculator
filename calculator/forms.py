from django import forms

CHOICES = [('sum', 'Addition'),
           ('sub', 'Subtraction'),
           ('mul', 'Multiplication'),
           ('div', 'Division'),
           ('fact', 'Factorial'),
           ('sqrt', 'Square root')]


class CalculatorForm(forms.Form):
    operation_type = forms.ChoiceField(choices=CHOICES, label='Operation type', widget=forms.RadioSelect)
    arguments = forms.JSONField(label='Arguments', initial=[])
