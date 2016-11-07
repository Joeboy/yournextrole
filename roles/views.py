import random

from django.shortcuts import render

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
    level = random.choice(levels)

    agent_noun = AgentNoun.objects.raw('''
        select * from {0} limit 1
        offset floor(random() * (select count(*) from {0}))
    '''.format(AgentNoun._meta.db_table))[0]

    homonym = Homonym.objects.raw('''
        select * from {0} limit 1
        offset floor(random() * (select count(*) from {0}))
    '''.format(Homonym._meta.db_table))[0]

    return render(request, 'home.html', context={
        'level': level,
        'agent_noun': agent_noun.word,
        'noun': homonym.word
    })
