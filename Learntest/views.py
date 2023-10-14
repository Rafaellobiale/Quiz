from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView
from itertools import chain

from .forms import (UserProfileForm, NoteForm, CustomUserCreationForm, QuestionForm, AddMultipleForm,
                    SingleChoiceQuestionForm)
from .models import UserProfile, Note, Question, MultiQuesModel, Answer, SingleChoiceQuestion, SingleQuestion


# This class must be changed into Notes and will take care of notes.html
class QuestionView(View):
    def get(self, request):
        all_items = Question.objects.all()  # Access to items from database Nur 1 .get(id=1); .filter(name='Hello')
        return render(request, "notes.html", {"all_items": all_items})  # variable into html file convey.

    def post(self, request):
        if request.method == "POST":
            print("Received data:", request.POST["itemName"])
            Question.objects.create(name=request.POST["itemName"])
            return redirect("/mylist")  # "mylist" or "/mylist"?
            # return self.get(request) #Redirect to the GET view having handled the POST request.


# This class must be changed into Notes and will take care of notes.html
class EditQuestionView(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        new_question_text = request.POST.get("question_text", "")
        if new_question_text:
            question.name = new_question_text
            question.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})


# This class must be changed into Notes and will take care of notes.html
class DeleteQuestionView(View):
    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
        except Question.DoesNotExist:
            pass

        return redirect("mylist")  # Redirect zur Frageübersichtsseite


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# Main page with empty "".
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class RegisterView(CreateView):
    form_class = CustomUserCreationForm  # Verwenden Sie Ihr benutzerdefiniertes Formular
    template_name = "registration.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # Saving the user in the database
        user = form.save()
        # User's login
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("index")  # Hier 'index' durch den Namen Ihrer Startseite ersetzen
    redirect_authenticated_user = True  # Dies leitet angemeldete Benutzer zur Startseite weiter

# ===================================================
# Questions' deletion and edition in separate htmls & urls

class QuestionManagerView(LoginRequiredMixin, TemplateView):
    template_name = "questionmanager.html"
    context_object_name = "questions"

    # Fetching data from database:
    def get_queryset(self):
        multi_questions = MultiQuesModel.objects.all()
        single_choice_questions = SingleChoiceQuestion.objects.all()
        text_questions = SingleQuestion.objects.all()

        # Debugging: Add print statements to check data
        print("Multi Questions:", multi_questions)
        print("Single Choice Questions:", single_choice_questions)
        print("Text Questions:", text_questions)

        return {"multi_questions": multi_questions, "single_choice_questions": single_choice_questions,
                "text_questions": text_questions}

    # # Add this method to handle form submissions
    # def post(self, request, *args, **kwargs):
    #     # Process form data here
    #
    #     # Debugging: Print form data
    #     answers_data = request.POST
    #     print("Form Data:", answers_data)
    #
    #     # Validate the form
    #     form = YourFormHere(request.POST)
    #     print("Form is Valid:", form.is_valid())
    #     print("Form Errors:", form.errors)
    #
    #     if form.is_valid():
    #         pass # Process the form data
    #
    #     return super().get(request, *args, **kwargs)  # Or redirect to another page


class DeleteMultiQuestionView(DeleteView):
    model = MultiQuesModel

    def get_success_url(self):
        return reverse("question_manager")


class DeleteSingleQuestionView(DeleteView):
    model = SingleChoiceQuestion

    def get_success_url(self):
        return reverse("question_manager")


class DeleteTextQuestionView(DeleteView):
    model = SingleQuestion

    def get_success_url(self):
        return reverse("question_manager")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['multi_questions'] = MultiQuesModel.objects.all()
    #     context['single_choice_questions'] = SingleChoiceQuestion.objects.all()
    #     context['text_questions'] = SingleQuestion.objects.all()
    #     return context

# ------------------------------------------
# Verwenden Sie das richtige Modell je nachdem, ob es sich um eine Multi-Choice MultiQuesModel,
# Single-Choice SingleChoiceQuestion oder Textfrage SingleQuestion handelt

class EditQuestionView(LoginRequiredMixin, UpdateView):
    template_name = "edit_question.html"
    context_object_name = "question"
    model = None


    def get_object(self, queryset=None):
        question_type = self.kwargs.get(
            "question_type")  # Addition of question type to url needed //den Fragetyp zu erkennen
        question_id = self.kwargs.get("pk")  # Get id from the question

        if question_type == "multi":
            self.model = MultiQuesModel
        elif question_type == "single":
            self.model = SingleChoiceQuestion
        elif question_type == "text":
            self.model = SingleQuestion

        return self.model.objects.get(pk=question_id)

    def get_success_url(self):
        question_type = self.kwargs.get("question_type")
        if question_type == "multi":
            return reverse("question_manager")
        elif question_type == "single":
            return reverse("question_manager")
        elif question_type == "text":
            return reverse("question_manager")

# =========================================================

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("index")  # Hier 'index' durch den Namen Ihrer Startseite ersetzen


# Notes.html
# class NotesView(View):
#     def get(self, request):
#         return render(request, "notes.html")


# This option is more
# preferred because it makes the code cleaner and more maintainable. For example, if you need to change
# the template, you can do so in a central place in the class without changing all the code in the get method.
# It also promotes the separation of logic and presentation, which is a proven pattern in web development.
# notes will be posted for all.
class NotesView(View):
    template_name = "notes.html"

    def get(self, request):
        return render(request, self.template_name)


# Formulaire for text question form


class QuestionFormView(FormView):
    template_name = "formular.html"
    form_class = QuestionForm
    success_url = reverse_lazy('success_page')

    def form_valid(self, form):
        # Hier kannst du die Verarbeitung durchführen, wenn das Formular gültig ist
        # Nach der Verarbeitung erfolgt eine Umleitung zur Erfolgsseite
        form.save()  # Speichert die Frage und die Antwort in der Datenbank
        return super().form_valid(form)

# class QuestionFormView(View):
#     template_name = "formular.html"
#     success_url = "success_page"  # 'success_page'
#
#     def get(self, request):
#         form = QuestionForm()
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request):
#         form = QuestionForm(request.POST)
#         if form.is_valid():  # Error
#             form.save()  # Speichert die Frage und die Antwort in der Datenbank
#             return redirect(self.success_url)  # Leiten Sie zur Erfolgsseite weiter
#         return render(request, self.template_name, {"form": form})

# ---------------------------------------------------------------------------
# Multiple Question test View
# You can begin the quiz here

class MultiHomeView(View):
    def get(self, request):
        # Lade alle Frage-Typen: Multi, Single und Text
        multi_questions = MultiQuesModel.objects.all()
        single_choice_questions = SingleChoiceQuestion.objects.all()
        text_questions = SingleQuestion.objects.all()

        questions = list(chain(multi_questions, single_choice_questions, text_questions))

        context = {"questions": questions}
        return render(request, "multihome.html", context)

    def post(self, request):
        if request.method == "POST":
            print(request.POST)
            valid_ids = [key for key in request.POST.keys() if key.isdigit()]  # Nur gültige IDs auswählen
            questions = Question.objects.filter(id__in=valid_ids)
            score = 0
            correct = 0
            wrong = 0
            total = len(questions)

            for q in questions:
                selected_answer = request.POST.get(str(q.id))
                if selected_answer:
                    selected_option = Option.objects.get(id=int(selected_answer))
                    if selected_option.is_correct:
                        score += 10
                        correct += 1
                    else:
                        wrong += 1
            if total > 0:
                percent = (score/ (total *10)) * 100
            else:
                percent = 0

            context = {
                "score": score,
                "time": request.POST.get("timer"),
                "correct": correct,
                "wrong": wrong,
                "percent": percent,
                "total": total,
            }
            return render(request, "result.html", context)


# Adding multi-question creation  class view
# multiformular.html forms.py  class AddMultipleForm(forms.ModelForm): models.py class MultiQuesModel(models.Model): views.py class AddMultiQuestionView(View):
class AddMultiQuestionView(View):
    def get(self, request):
        if request.user.is_staff:
            form = AddMultipleForm()
            context = {"form": form}
            return render(request, "multiformular.html", context)
        else:
            return redirect("index")

    def post(self, request):
        if request.user.is_staff:
            form = AddMultipleForm(request.POST)
            print(request.POST)  # Hier printen Sie die POST-Daten
            print(form.is_valid())  # Hier printen Sie, ob das Formular gültig ist
            print(form.errors)  # Hier printen Sie eventuelle Formularfehler

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()

                answers_data = form.cleaned_data["answers"]
                print(answers_data) # Hier printen Sie die geparsten Antwortdaten
                for answer_data in answers_data:
                    answer_text = answer_data["text"]
                    is_correct = answer_data["is_correct"]

                    answer, _ = Answer.objects.get_or_create(text=answer_text)
                    instance.answers.add(answer, through_defaults={"is_correct": is_correct})
                print("Preparing to redirect...")  # Data shown, that redirect is on its way. Hier wird geprintet, dass Sie sich auf die Weiterleitung vorbereiten
                return redirect("success_page")
            else:
                return render(request, "multiformular.html", {"form": form})
        else:
            return redirect("index")


# Page gets displayed once question is added successfully.
class SuccessPageView(View):
    template_name = "success_page.html"
    return_url = "success_page"  # Verweist auf den Namen der URL "question_manager"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return HttpResponseRedirect(reverse(self.return_url))


# Single choice question
# --------------------------------
class AddSingleChoiceQuestionView(View):
    template_name = "single_choice_form.html"

    def get(self, request):
        form = SingleChoiceQuestionForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_staff:
            form = SingleChoiceQuestionForm(request.POST)
            print(request.POST)
            print(form.is_valid())
            print(form.errors)
            if form.is_valid():
                question = form.save()

                # Inspect the selected options from Checkboxes. Ermitteln Sie die ausgewählte Option aus den Checkboxen
                selected_option = int(request.POST.get("correct_option"))

                for i in range(1, 6):
                    option_text = request.POST.get(f"option_{i}")
                    is_correct = i == selected_option  # Checks if one option is chosen. Überprüft, ob diese Option die ausgewählte ist
                    question.singlechoiceoption_set.create(option_text=option_text, is_correct=is_correct)

                # return HttpResponseRedirect("success_page")
                return redirect("success_page")

            return render(request, self.template_name, {"form": form})
        else:
            return redirect("index")

# -----------------------------------------------------------------

class QuizDataView(View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk) # pk=2
        questions = [] # questions = quiz.get_questions(number_of_questions=5)

        for q in quiz.get_questions():
            answers = []

            for ans in q.get_answers():
                answers.append(ans.answer_text)

            questions.append({str(q): answers})

        return JsonResponse({
            'data': questions,
            'time': quiz.time,
        })

# def quiz_data_view(request, pk):
#     quiz - Quiz.objects.get(pk=pk)
#     questions = []
#     for q in quiz.get_questions():
#         answers = []
#         for ans in q.get_answers():
#             answers.append(ans.answer_text)
#         questions.append({str(q): answers})
#     return JsonResponse({
#         'data' :questions,
#         'time': quiz.time,
#     })


# -----------------------------------------------------------------

# my_account.html creates a place for a user to store notes, change the password and
# to edit posted note.
# name="dispatch" is optional Argument for @method_decorator, which specifies which method of the view is to be decorated.
@method_decorator(login_required, name="dispatch")
class MyAccountView(View):
    template_name = "my_account.html"

    def get(self, request):
        password_form = PasswordChangeForm(request.user)
        note_form = NoteForm()
        notes = Note.objects.filter(user=request.user)

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

        user_profile_form = UserProfileForm(instance=user_profile)

        context = {"password_form": password_form, "note_form": note_form, "notes": notes, "user_profile": user_profile, "user_profile_form": user_profile_form, }

        return render(request, self.template_name, context)

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)
        note_form = NoteForm(request.POST)
        # Initialisieren Sie user_profile mit None, um sicherzustellen, dass es in jedem Fall eine Zuweisung gibt.
        user_profile = None

        if "change_password" in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Ihr Passwort wurde erfolgreich geändert.")
                return redirect("my_account")
            else:
                messages.error(request, "Fehler beim Aendern des Passworts. Bitte ueberpruefen Eingaben.")
                return HttpResponseRedirect(reverse("my_account"))
        print(request.POST)
        if "save_profile" in request.POST:    # DeBugger
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.preferred_language = request.POST.get("preferred_language", "")
            user_profile.save()

            messages.success(request, "Ihr Profil wurde erfolgreich aktualisiert.")

        # Falls weder das Passwortformular noch das Notizformular gültig sind,
        # leiten Sie den Benutzer zurück zur MyAccount-Seite mit den Fehlermeldungen.
        notes = Note.objects.filter(user=request.user)
        context = {
            "password_form": password_form,
            "note_form": note_form,
            "notes": notes,
            "user_profile": user_profile,
        }
        return render(request, self.template_name, context)


