from django.shortcuts import render
from django.shortcuts import redirect, reverse 
import random
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.core import serializers
# Create your views here.
#GLOBAL VARS
repeat_list = []






def index(request):
    global mode
    mode='ordered'
    sentence_name = Sentence.objects.filter(state='hot').order_by('revision_number').first()
    sentence = Sentence.objects.get(name=str(sentence_name))
    rest_count = Sentence.objects.filter(state='hot',revision_number=0).count()
    context = {
        'sentence': sentence,
        'rest_count': rest_count

    }
    return render(request, 'index.html', context)

def repeat(request):
    sentence_list = Sentence.objects.filter(type='expression')
    global repeat_list
    if len(repeat_list) >= len(sentence_list) - 3:
        repeat_list = []
    while True:
        rid = random.randint(0, len(sentence_list) - 1)
        if rid in repeat_list:
            continue
        else:
            break
    repeat_list = repeat_list + [rid]
    sentence1 = Sentence.objects.get(name=sentence_list[rid])
    while True:
        rid = random.randint(0, len(sentence_list) - 1)
        if rid in repeat_list:
            continue
        else:
            break
    repeat_list = repeat_list + [rid]

    sentence2 = Sentence.objects.get(name=sentence_list[rid])
    while True:
        rid = random.randint(0, len(sentence_list) - 1)
        if rid in repeat_list:
            continue
        else:
            break    
    repeat_list = repeat_list + [rid]
    sentence3 = Sentence.objects.get(name=sentence_list[rid])
    context = {
        'sentence1': sentence1,
        'sentence2': sentence2,
        'sentence3': sentence3,

    }

    return render(request, 'repeat.html', context)

def random_hot(request):
    global mode
    mode='random'
    sentence_list = Sentence.objects.filter(state='hot')
    rid = random.randint(0, len(sentence_list) - 1)
    sentence = Sentence.objects.get(name=sentence_list[rid])
    rest_count = Sentence.objects.filter(state='hot',revision_number=0).count()


    context = {
        'sentence': sentence,
        'rest_count': rest_count
        

    }
    return render(request, 'index.html', context)


def promote(request, id):
    sentence = Sentence.objects.get(pk=id)
    revision_number = getattr (sentence, 'revision_number')

    setattr (sentence, 'state', 'hot')
    setattr (sentence, 'revision_number', revision_number + 1 )
    sentence.save()
    if mode == 'ordered':
        return redirect('/')
    elif mode == 'random':
        return redirect('/random')


def demote(request, id):
    sentence = Sentence.objects.get(pk=id)
    setattr (sentence, 'state', 'cold')
    sentence.save()
    if mode == 'ordered':
        return redirect('/')
    elif mode == 'random':
        return redirect('/random')
    
