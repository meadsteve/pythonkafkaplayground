from django.http import HttpResponse
from django.template import loader
from .models import RandomRun, RandomEntry

def index(request):
    run_list = RandomRun.objects.all()
    template = loader.get_template('run_list.html')
    context = {
        'run_list': run_list,
    }
    return HttpResponse(template.render(context, request))

def entry_list(request, run_id):
    random_run = RandomRun.objects.get(run_id=run_id)
    random_entry_list = RandomEntry.objects.all().filter(random_run=random_run)
    template = loader.get_template('data_list.html')
    context = {
        'random_entry_list': random_entry_list,
    }
    return HttpResponse(template.render(context, request))
