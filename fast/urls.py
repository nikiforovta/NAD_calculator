from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<operation>/', views.fast_operation, name='fast operation'),
]
