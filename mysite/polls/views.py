from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'  # specific variables model, context_object_name, and template_name need to be set like we did here or well we will get something created by Django

    def get_queryset(self):
        return Question.objects.filter(publication_date__lte=timezone.now()).order_by('-publication_date')[:5]  # lte <= gte >=, making sure to only query published dates not in future.


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(publication_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.choice_set.all  # I can do this since Question is a ForeignKey argument of Choice in models



def vote(request, question_id): # request contains data for the actual vote choice
    question = get_object_or_404(Question, pk=question_id) # grabbing the Question object where primary key = question id, will return 404 error if failed
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # request.post is a dictionary, we are accessing data by using 'choice' as a key
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  # should return something like /polls/3/results 3 = question_id


    # Create your views here.
