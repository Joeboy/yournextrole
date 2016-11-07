from django.db import models


class Homonym(models.Model):
    word = models.TextField(unique=True)

    def __str__(self):
        return self.word

class AgentNoun(models.Model):
    word = models.TextField(unique=True)

    def __str__(self):
        return self.word
