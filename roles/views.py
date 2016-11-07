import random

from django.shortcuts import render
from django.http import JsonResponse

from roles.models import Homonym, AgentNoun


levels = [
    'senior',
    'junior',
    'rockstar',
    'acting',
    'lead',
    'quantitative',
    'full stack',
]


def home(request):
    level = request.GET.get('level', random.choice(levels))

    agent_noun = request.GET.get('agent_noun', AgentNoun.objects.raw('''
        select * from {0} limit 1
        offset floor(random() * (select count(*) from {0}))
    '''.format(AgentNoun._meta.db_table))[0].word)

    homonym = request.GET.get('noun', Homonym.objects.raw('''
        select * from {0} limit 1
        offset floor(random() * (select count(*) from {0}))
    '''.format(Homonym._meta.db_table))[0].word)

    context = {
        'level': level,
        'agent_noun': agent_noun,
        'noun': homonym
    }

    if request.is_ajax():
        return JsonResponse(context)

    return render(request, 'home.html', context=context)
