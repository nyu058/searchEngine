from django.shortcuts import render
from django.http import HttpResponse
import os.path
from django.template import Context, loader

def index(request):
    template= loader.get_template('index.html')
    return HttpResponse(template.render())
