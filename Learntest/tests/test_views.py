import pytest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from ..models import MultiQuesModel, Answer, SingleChoiceQuestion
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


from ..views import AddMultiQuestionView, QuestionFormView, RegisterView, CustomLoginView, CustomUserCreationForm
from ..forms import AddMultipleForm, SingleChoiceQuestionForm, QuestionForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

User = get_user_model()
CustomUser = get_user_model()
UserProfile = get_user_model()
#-----------------------------------------------------------

# pytest -k "multichoice"    pytest -k "multichoice" -v
@pytest.mark.django_db
class TestAddMultiQuestionView:

    @pytest.mark.multichoice
    def test_view_requires_staff_login(self, client):
        url = reverse("multiform")
        response = client.get(url)
        assert response.status_code == 302  # Erwartet eine Weiterleitung (Redirect)

    def test_view_displays_form_for_staff_user(self, client, staff_user):
        client.login(username='staffuser', password='staffpassword')
        url = reverse("multiform")
        response = client.get(url)
        assert response.status_code == 200
        assert "Number of Answers Anzahl der Antworten" in str(response.content)

    def test_add_multi_question(self, client, staff_user):
        client.login(username='staffuser', password='staffpassword')
        url = reverse("multiform")
        data = {
            "question": "Test question",
            "language_name": 2,  # Passen Sie dies entsprechend Ihrer Datenbank an
            "ans_count": 3,
            "answer_0": "Option 1",
            "is_correct_0": True,
            "answer_1": "Option 2",
            "is_correct_1": False,
            "answer_2": "Option 3",
            "is_correct_2": True,
        }
        print("Sending POST request to the view...")
        response = client.post(url, data)
        print("Received response from the view:", response)
        print(response.content)         # Hinzugefügter Code: Printen Sie den Inhalt der Antwort
        assert response.status_code == 302  # 302 Erwartet eine Weiterleitung (Redirect)
        assert MultiQuesModel.objects.count() == 1
        assert Answer.objects.count() == 2

# ------------------------------------------------------------------------
# Single choice question

# pytest -k "singlechoice"   pytest -k "singlechoice" -v
@pytest.mark.django_db
class TestAddSingleChoiceQuestion:

    @pytest.mark.singlechoice
    def test_add_single_choice_question(self, client, staff_user):
        client.login(username='staffuser', password='staffpassword')
        url = reverse("singleform")  # Ersetzen Sie "singlechoice_form" durch den tatsächlichen Namen Ihrer URL-Entsprechung
        data = {
            "question_text": "Pytest's question",
            "language_name": 2,
            "correct_option": 3,  # Passen Sie die ausgewählte Option an
            "option_1": "Option 1",
            "option_2": "Option 2",
            "option_3": "Option 3",
            "option_4": "Option 4",
            "option_5": "Option 5",
        }

        print("Sending POST request to the view...")
        response = client.post(url, data)
        print("Received response from the view:", response)
        print(response.content)  # Hinzugefügter Code: Drucken Sie den Inhalt der Antwort

        # Überprüfen Sie die Statuscode und die erwartete Weiterleitung
        assert response.status_code == 302  # Erwartet eine Weiterleitung (Redirect)
        assert response.url == reverse("success_page")  # Erwartet eine Weiterleitung zur "success_page"

        # Fügen Sie weitere Prüfungen hinzu, um sicherzustellen, dass die Daten korrekt in der Datenbank gespeichert wurden, falls erforderlich.
        # Hier könnte Ihre Datenbankabfrage aussehen, um sicherzustellen, dass die Frage und Optionen korrekt erstellt wurden.
        question = SingleChoiceQuestion.objects.get(question_text="Test question")
        assert question is not None
        options = question.singlechoiceoption_set.all()
        assert options.count() == 5
        # Fügen Sie weitere Prüfungen für Optionen hinzu, um sicherzustellen, dass die richtige Option als korrekt markiert ist.





        # # Check if the view redirects to the success page after a successful POST request
        # assert response.status_code == 302  # 302 is the HTTP status code for a redirection
        # assert response.url == reverse('success_page')  # Adjust this to your specific view name
        #
        # # Check if the created question exists in the database
        # assert SingleChoiceQuestion.objects.filter(question_text='Test Question').exists()
        #
        # # Überprüfen Sie die Statuscode und die erwartete Weiterleitung
        # assert response.status_code == 302  # Erwartet eine Weiterleitung (Redirect)
        # assert response.url == reverse("success_page")  # Erwartet eine Weiterleitung zur "success_page"
        #
        # # Fügen Sie weitere Prüfungen hinzu, um sicherzustellen, dass die Daten korrekt in der Datenbank gespeichert wurden, falls erforderlich.
        # # Hier könnte Ihre Datenbankabfrage aussehen, um sicherzustellen, dass die Frage und Optionen korrekt erstellt wurden.
        # question = SingleChoiceQuestion.objects.get(question_text="Test question")
        # assert question is not None
        # options = question.singlechoiceoption_set.all()
        # assert options.count() == 5
        # # Fügen Sie weitere Prüfungen für Optionen hinzu, um sicherzustellen, dass die richtige Option als korrekt markiert ist.

# ========================================================================================
# Text question test
# inherits from TestCase no need to add db mark.
# pytest -k "formview"    pytest -k "formview" -v

class TestQuestionFormView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    @pytest.mark.text  # passed
    def test_get_request_displays_form(self):
        url = reverse("question_form")
        request = self.factory.get(url)
        self.client.force_login(self.user)
        response = self.client.get(url)

        print("Sending GET request to the view...")
        print("Received response from the view:", response)
        print(response.content)

        self.assertEqual(response.status_code, 200)

        #Failed 200 != 302
    def test_post_request_with_valid_form_redirects_to_success_page(self):
        url = reverse("question_form")
        data = {
            "question_text": "Test question"
        }
        request = self.factory.post(url, data)
        self.client.force_login(self.user)
        response = self.client.post(url, data)

        print("Sending POST request to the view...")
        print("Received response from the view:", response)
        print(response.content)

        self.assertRedirects(response, reverse('success_page'), fetch_redirect_response=False)

        # passed
    def test_post_request_with_invalid_form_displays_form_again(self):
        url = reverse("question_form")
        data = {}
        request = self.factory.post(url, data)
        self.client.force_login(self.user)
        response = self.client.post(url, data)

        print("Sending POST request to the view...")
        print("Received response from the view:", response)
        print(response.content)

        self.assertEqual(response.status_code, 200)


# =========================================
# pytest -k "register" -v
# Passes

@pytest.mark.register
@pytest.mark.django_db
class TestRegisterView:

    def test_register_view(self, client):
        user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # Erstellen Sie ein Formulardaten-Dikt
        form_data = {
            'username': user_data['username'],
            'password1': user_data['password1'],
            'password2': user_data['password2'],
        }

        # Verwenden Sie die client.post()-Methode, um die POST-Anfrage zu erstellen
        response = client.post(reverse('register'), data=form_data)

        # Aktualisieren Sie diesen Wert mit dem erwarteten HTTP-Statuscode
        expected_status_code = 302  # Hier den erwarteten HTTP-Statuscode für die Weiterleitung eintragen

        # Überprüfen Sie, ob der tatsächliche Statuscode dem erwarteten Statuscode entspricht
        assert response.status_code == expected_status_code

        # Überprüfen Sie, ob die Weiterleitung zur Anmeldeseite erfolgt
        assert '/accounts/login/' in response.url

#===========================================================

# pytest -k "login" -v


@pytest.mark.django_db
class TestCustomLoginView:

    @pytest.mark.login
    # Define the method to ensure that the login.html view is used as a template.
    def test_template_name(self, client):
        response = client.get(reverse("login"))
        # assert "login.html" in [template.name for template in response.templates] # FAILED tests/test_views.py::TestCustomLoginView::test_template_name - AssertionError: assert 'login.html' in ['registration/login.html', 'navbar.html']
        assert response.template_name == ['login.html']

    # Define the method to ensure that the view redirects logged-in users to the home page:
    def test_redirect_authenticated_user(self, client):
        # Erstellen und anmelden eines Benutzers
        # Testet, ob angemeldete Benutzer zur Startseite weitergeleitet werden
        # Führt die Anmeldung des Benutzers durch, bevor die Anfrage gestellt wird.
        User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')

        response = client.get(reverse("login"))
        assert response.status_code == 302  # Redirection awaited # FAILED tests/test_views.py::TestCustomLoginView::test_redirect_authenticated_user - assert 200 == 302

        assert response.url == reverse("index")  # Erwartete Weiterleitung zur Startseite

        # ----------Alternative----------------------------
        # user = User.objects.create_user(username='testuser', password='testpassword')
        # client.login(username='testuser', password='testpassword')
        # response = client.get(reverse('login'))
        # assert response.status_code == 302  # 302 ist der HTTP-Statuscode für eine Weiterleitung
        #--------------------------------------------------


# ------------Other version functional version Text question test----------------------
# @pytest.mark.django_db
# class TestQuestionFormView:
#
#     @pytest.mark.formview
#     def test_get_request_displays_form(self):
#         factory = RequestFactory()
#         request = factory.get(reverse("question_form"))
#         view = QuestionFormView.as_view()
#         response = view(request)
#
#         assert response.status_code == 200
#         content = response.content.decode("utf-8")  # Dekodieren des Antwortinhalts in Text
#         assert "form" in content  # Überprüfe, ob "form" im Antwortinhalt enthalten ist
#
#         print("Sending GET request to the view...")
#         print("Received response from the view:", response)
#         print(response.content)
#
#     def test_post_request_with_valid_form_redirects_to_success_page(self):
#         factory = RequestFactory()
#         request = factory.post(reverse("question_form"), data={"question_text": "Test question"})
#         view = QuestionFormView.as_view()
#         response = view(request)
#
#         assert isinstance(response, HttpResponseRedirect)
#         # assert response.url == reverse("success_page")
#
#         print("Sending POST request to the view...")
#         print("Received response from the view:", response)
#         print(response.content)
#
#     def test_post_request_with_invalid_form_displays_form_again(self):
#         factory = RequestFactory()
#         request = factory.post(reverse("question_form"), data={})
#         view = QuestionFormView.as_view()
#         response = view(request)
#
#         assert response.status_code == 200
#         content = response.content.decode("utf-8")  # Dekodieren des Antwortinhalts in Text
#         assert "form" in content  # Überprüfe, ob "form" im Antwortinhalt enthalten ist
#
#         print("Sending POST request to the view...")
#         print("Received response from the view:", response)
#         print(response.content)
