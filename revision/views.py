from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.core import serializers
# Create your views here.

def index(request):
    sentence_name = Sentence.objects.filter(state='hot').order_by('revision_number').first()
    sentence = Sentence.objects.get(name=str(sentence_name))

    context = {
        'sentence': sentence

    }
    return render(request, 'index.html', context)