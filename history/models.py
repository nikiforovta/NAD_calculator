import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

User = get_user_model()


class Entry(models.Model):
    OPERATION_TYPES = (
        ('sum', 'Sum'),
        ('sub', 'Subtraction'),
        ('div', 'Division'),
        ('mul', 'Multiplication'),
        ('sqrt', 'Square root'),
        ('fact', 'Factorial')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=4, choices=OPERATION_TYPES)
    operands = ArrayField(base_field=models.FloatField())
    result = ArrayField(base_field=models.FloatField())
    message = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f'User {self.user} calculating {self.operation_type} of {self.operands} (id: {self.id})\tResult: {self.result}'
