"""
URL configuration for Quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from Learntest.views import (
    QuestionView,
    IndexView,
    DeleteQuestionView,
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    QuestionManagerView,
    EditQuestionView,
    QuestionFormView,
    SuccessPageView,
    AddMultiQuestionView,
    MultiHomeView,
    AddSingleChoiceQuestionView,
    NotesView,
    MyAccountView,
    QuizDataView,
# Editing in separate urls & html files
    EditQuestionView,
    DeleteMultiQuestionView,
    DeleteSingleQuestionView,
    DeleteTextQuestionView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", IndexView.as_view(), name="index"),
    path("mylist/", QuestionView.as_view(), name="mylist"),
    path(
        "mylist/delete/<int:question_id>/", DeleteQuestionView.as_view(), name="delete_question"
    ),  # Hinzufügen einer URL zum Löschen
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("mylist/edit/<int:question_id>/", EditQuestionView.as_view(), name="edit_question"),
    path(
        "questionmanager/", QuestionManagerView.as_view(), name="question_manager" # All questions ought to appear here.
    ),  # Hier "question_manager" als Name verwenden
    path("question-form/", QuestionFormView.as_view(), name="question_form"), # formular.html text question
    # Multi question form.
    path("multi-form/", AddMultiQuestionView.as_view(), name="multiform"),  # 'multiformular.html'
    path("multi-site/", MultiHomeView.as_view(), name="multihome"),  # Site to begin the quiz
    path("single-form/", AddSingleChoiceQuestionView.as_view(), name="singleform"), # single_choice_form.html
    path("success-page/", SuccessPageView.as_view(), name="success_page"),  # success_page.html Erfolgsseite
    path("notes/", NotesView.as_view(), name="notes"),
    path("my-account/", MyAccountView.as_view(), name="my_account"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),  # redirect to login.html
# Quesions' answers' view The responses are to be displayed here multihome.html
#     path("multi-site/data/<int:pk>/", QuizDataView.as_view(), name="multihome"), # different name
    path("multi-site/<int:pk>/", QuizDataView.as_view(), name="multihome"), # different name

# Edition, deletion of questions in separete urls&html files

    path("questionmanager/edit/<int:pk>/", EditQuestionView.as_view(), name="edit_question"), #edit_question.html
    path("questionmanager/multi/delete/<int:pk>/", DeleteMultiQuestionView.as_view(), name="delete_multi_question"),
    path("questionmanager/single/delete/<int:pk>/", DeleteSingleQuestionView.as_view(), name="delete_single_question"),
    path("questionmanager/text/delete/<int:pk>/", DeleteTextQuestionView.as_view(), name="delete_text_question"),


]
