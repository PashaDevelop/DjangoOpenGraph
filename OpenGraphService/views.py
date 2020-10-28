"""
Модуль для отдачи на клиент сформированного OpenGraph
"""
from typing import Union

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from .opengraph import OpenGraph


def index(request: HttpRequest) -> HttpResponse:
    """
    Стартовая страница
    """
    return render(request, 'index.html')


def parse_from_url(request: HttpRequest) -> Union[HttpResponse, HttpResponseBadRequest]:
    """
    Формирует OpenGraph из url, пришедшего в GET параметре url
    :return: OpenGraph в формате json
    """
    url = request.GET['url']
    try:
        graph = OpenGraph(url=url)
    except (ValueError, AttributeError):
        return HttpResponseBadRequest('Не удалось сформировать OpenGraph. Страничка невалидна.')
    if not graph.is_valid():
        return HttpResponseBadRequest('Данная веб-страничка не отвечает требованиям OpenGraph')
    return HttpResponse(content=graph.to_json(), status=200, content_type='application/json')


def view(request):
    pass


def view2(request):
    pass


def view3(request):
    pass
