from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from polls.models import Choice, Poll
from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, {
    #    'latest_question_list': latest_question_list,
    #})
    context = {'latest_question_list': latest_question_list}
    #output = ', '.join([p.question for p in latest_question_list])
    #return HttpResponse(output)
    #return HttpResponse(template.render(context))
    return render(request, 'polls/index.html', context)

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


def detail(request, question_id):
    #return HttpResponse("You're looking at question %s." % question_id)
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def results(request, question_id):
    poll = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay teh poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. this prevents data from being posted twice if a
        # user hits de Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

    #return HttpResponse(response)
