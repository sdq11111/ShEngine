from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse

def search(request):
    return render(request, 'index.html')
