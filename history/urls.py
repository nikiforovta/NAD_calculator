from django.urls import path

from history.views import *

urlpatterns = [
    path('', index, name='index'),
    path('<uuid:operation_id>', operation, name='operation'),
    path('remove/<uuid:operation_id>', remove, name='remove_operation'),
    path('entry/create/', EntryCreateView.as_view()),
    path('all/', EntriesListView.as_view()),
    path('entry/detail/<uuid:pk>/', EntryDetailView.as_view()),
    path('entry/get/<operation_id>', operation, name='operation'),
    path('result/<operation_id>', get_result, name='result'),
    path('entry/remove/<operation_id>', remove, name='remove')
]
