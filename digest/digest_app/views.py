from django.shortcuts import render
from .parsings.common_interface import get_news

def index(request):
    news = get_news()
    print(news)
    return render(request, 'index.html')