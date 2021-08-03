from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))
    #return render(request, 'polls/index.html, context) this is the shortcut to rendering


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question Does not Exist')
    return render(request, 'polls/detail.html', {'question': question})

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})    

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question' : question})
      


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selsected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selsected_choice.votes += 1  
        selsected_choice.save()  
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))    

