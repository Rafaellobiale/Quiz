from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User, Permission
import random
# from django.contrib.contenttypes.models import ContentType for Permissionrequired
# from django.apps import apps

# Create your models here.

# This class is for Plus button. Will be modified- it will give possibility to add notes etc. It will be relocated to another page.
# To be changed into class Notes
class Question(models.Model):
    created_at = models.DateField(default=date.today)
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + self.name  # Name will be shown with id.



# This class will be used for text question.
class SingleQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    answer_text = models.CharField(max_length=255)  # Neues Feld für die Antwort

    language_name = models.ForeignKey(
        "Category", on_delete=models.CASCADE
    )  # One to many relation; ForeignKey-Beziehung zu Category
    question_type = models.ForeignKey("QuestionType", on_delete=models.CASCADE)
    # # One to many relation; ForeignKey-Beziehung zu Category

    def __str__(self):
        return self.question_text

    def get_answers(self):
        return self.answer_text_set.all()


# These classes are needed for a dropdown selection of programming languages and question_type, which are added manually in the database with "+".
class Category(models.Model):
    language_name = models.CharField(max_length=100, unique=True, default="")  # One to many in Single Question

    def __str__(self):
        return self.language_name

class QuestionType(models.Model):
    question_type = models.CharField(max_length=100, unique=True, default="")

    def __str__(self):
        return self.question_type

# ----------------------------------------------------------
# Założenie już mamy ile odp jest poprawnych
# This is needed for visualisation of multi- question form
# User must specify how many answers are correct
# User can choose how many answers can be given.
# multiformular.html forms.py  class AddMultipleForm(forms.ModelForm): models.py class MultiQuesModel(models.Model): views.py class AddMultiQuestionView(View):
# Adding category of language
class MultiQuesModel(models.Model):
    question = models.CharField(max_length=200, null=True)
    answers = models.ManyToManyField("Answer", through="QuestionAnswer")

    language_name = models.ForeignKey("Category", on_delete=models.CASCADE)
    question_type = models.ForeignKey("QuestionType", on_delete=models.CASCADE)

    # One to many relation; ForeignKey-Beziehung zu Category

    def __str__(self):
        return self.question

    def get_answers(self):
        return self.answers_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class QuestionAnswer(models.Model):
    question = models.ForeignKey(MultiQuesModel, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

# --------------------------------------
# Single Choice question

class SingleChoiceQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    language_name = models.ForeignKey("Category", on_delete=models.CASCADE)
    question_type = models.ForeignKey("QuestionType", on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
# Getting answers for actual quiz at multihome.html
    def get_answers(self):
        return self.answer_set.all()


class SingleChoiceOption(models.Model):
    question = models.ForeignKey(SingleChoiceQuestion, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
# -------------------------------------------------------------
# Fetching and displaying the questions on multi-site multihome.html
class Quiz(models.Model):
    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score to pass")
    # difficulty = models.CharField(max_length=80, choices=DIFF_CHOICES) # Not defined yet
    # And other fields for your Quiz model
    class Meta:
        verbose_name_plural = "Quizes"

    def get_questions(self, number_of_questions):
        return self.question_set.all()[:number_of_questions]

# Posisbility to add random-question quiz
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]


# -------------------------------------------------------------
# For account tab
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return self.user.username


# --------------------------------------------------------
# Class to be verified!
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
