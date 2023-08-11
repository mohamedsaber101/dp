from django.shortcuts import render
from django.shortcuts import redirect, reverse 

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



def promote(request, id):
    sentence = Sentence.objects.get(pk=id)
    revision_number = getattr (sentence, 'revision_number')

    setattr (sentence, 'state', 'hot')
    setattr (sentence, 'revision_number', revision_number + 1 )
    sentence.save()
    return redirect('/')


def demote(request, id):
    sentence = Sentence.objects.get(pk=id)
    setattr (sentence, 'state', 'cold')
    sentence.save()
    return redirect('/')