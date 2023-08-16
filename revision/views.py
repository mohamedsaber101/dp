from django.shortcuts import render
from django.shortcuts import redirect, reverse 
import random
import datetime
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.core import serializers
# Create your views here.
#GLOBAL VARS
repeat_list = []
start_time = datetime.datetime.now()




def index(request):
    global mode 
    mode='ordered'
    global type
    type = 'index'
    sentence_name = Sentence.objects.filter(state='hot').order_by('revision_number').first()
    sentence = Sentence.objects.get(name=str(sentence_name))
    rest_count = Sentence.objects.filter(state='hot',revision_number=sentence.revision_number).count()
    context = {
        'sentence': sentence,
        'rest_count': rest_count,
        'timer': str((datetime.datetime.now() - start_time)).split('.')[0],


    }
    return render(request, 'index.html', context)

def vocabulary(request):
    global mode
    mode = 'vocabulary'
    sentence_name = Sentence.objects.filter(state='hot', type='vocabulary').order_by('revision_number').first()
    sentence = Sentence.objects.get(name=str(sentence_name))
    rest_count = Sentence.objects.filter(state='hot',revision_number=sentence.revision_number, type='vocabulary').count()
    context = {
        'sentence': sentence,
        'rest_count': rest_count,
        'timer': str((datetime.datetime.now() - start_time)).split('.')[0],

        

    }
    return render(request, 'index.html', context)


def inject(request):

    in_process_sentences = Sentence.objects.filter(state='hot', revision_number__lte='0')
    if len(in_process_sentences) > 0:
        print ('\n********* DP ********* '+ str(len(in_process_sentences)) + ' are still under processing. Complete them and come back\n')
        return redirect('/')
    else:
        indexed_episode = Index.objects.filter(state='pending').order_by('pk').first()
        data_rows = Sentence.objects.filter(name__contains = indexed_episode.name)
        for row in data_rows:
            setattr(row, 'state', 'hot')
            row.save()
        setattr(indexed_episode, 'state', 'injected')
        setattr(indexed_episode, 'time_of_injection', datetime.datetime.now())     
        indexed_episode.save()
        return redirect('/')



def delete(request, id):
    sentence = Sentence.objects.get(pk=id)
    sentence.delete()
    if mode == 'ordered':
        return redirect('/')
    elif mode == 'random':
        return redirect('/random')



def repeat(request):
    global mode
    mode = 'repeat'
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
        'timer': str((datetime.datetime.now() - start_time)).split('.')[0],

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
        'rest_count': rest_count,
        'timer': str((datetime.datetime.now() - start_time)).split('.')[0],

        

    }
    return render(request, 'index.html', context)


    
def promote(request, id):
    sentence = Sentence.objects.get(pk=id)
    revision_number = getattr (sentence, 'revision_number')

    setattr (sentence, 'state', 'hot')
    setattr (sentence, 'revision_number', revision_number + 1 )
    sentence.save()
    return next_action(request)



def demote(request, id):
    sentence = Sentence.objects.get(pk=id)
    setattr (sentence, 'state', 'cold')
    sentence.save()
    return next_action(request)


def next_action(request):
    if mode == 'ordered':
        return redirect('/')
    elif mode == 'random':
        return redirect('/random')
    elif mode == 'vocabulary':
        return redirect('/vocabulary')
    elif mode == 'repeat':
        return redirect('/repeat')
    
def set_timer(request):
    global start_time
    start_time = datetime.datetime.now()
    return next_action(request)
