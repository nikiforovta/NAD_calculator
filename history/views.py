from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rest_framework import generics
from rest_framework.decorators import api_view

from history.models import Entry
from history.permissions import IsOwner
from history.serializers import HistoryEntrySerializer, HistoryEntriesSerializer


class EntryCreateView(generics.CreateAPIView):
    """Создание записи в истории вычислений"""
    serializer_class = HistoryEntrySerializer


class EntriesListView(generics.ListAPIView):
    """Отображение истории вычислений для пользователя"""
    serializer_class = HistoryEntriesSerializer
    queryset = Entry.objects.all()
    permission_classes = (IsOwner,)


class EntryDetailView(generics.RetrieveDestroyAPIView):
    """Просмотр записи в истории вычислений с возможностью удаления"""
    serializer_class = HistoryEntrySerializer
    queryset = Entry.objects.all()
    permission_classes = (IsOwner,)


def index(request):
    template = loader.get_template('history/history.html')
    context = {'history': Entry.objects.filter(user=request.user)}
    return HttpResponse(template.render(context, request))


@api_view(["GET"])
@login_required(login_url='/auth/login')
def get_result(request, operation_id):
    template = loader.get_template('slow/result.html')
    result = Entry.objects.get(id=operation_id)
    if result.result == [0.0]:
        result.result = "Not ready yet, try again later"
    return HttpResponse(template.render({"result": result}, request))


@login_required(login_url='/auth/login')
def operation(request, operation_id):
    template = loader.get_template('history/history_entry.html')
    context = {'entry': Entry.objects.get(id=operation_id)}
    return HttpResponse(template.render(context, request))


def remove(request, operation_id):
    r = Entry.objects.get(id=operation_id)
    r.delete()
    return HttpResponseRedirect("../")
