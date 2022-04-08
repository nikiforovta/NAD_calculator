from django import forms

CHOICES = [('sum', 'Addition'),
           ('sub', 'Subtraction'),
           ('mul', 'Multiplication'),
           ('div', 'Division'),
           ('fact', 'Factorial'),
           ('sqrt', 'Square root')]


class CalculatorForm(forms.Form):
    operation_type = forms.ChoiceField(choices=CHOICES, label='Operation type', widget=forms.RadioSelect)
    arguments = forms.CharField(label='Arguments', widget=forms.Textarea)

    def is_valid(self):
        valid = super(CalculatorForm, self).is_valid()

        if not valid:
            return valid
        else:
            arguments = self.cleaned_data['arguments'].split('\r\n')
            return all([argument.replace('.', '', 1).lstrip("-").isdigit() for argument in arguments])