from django.db import models


class Question(models.Model):
    body = models.CharField(max_length=150)


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option = models.CharField(max_length=80)
    correct = models.BooleanField(default=False)
