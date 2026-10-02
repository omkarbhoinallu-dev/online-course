import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings

# <HINT> Question model
class Question(models.Model):
    courses = models.ManyToManyField('Course')
    question_text = models.CharField(max_length=500)
    grade = models.FloatField(default=1.0)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True, blank=True)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_incorrect == 0:
            return True
        return False

    def __str__(self):
        return self.question_text

# <HINT> Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

# <HINT> Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)