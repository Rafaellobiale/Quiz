from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Importiere das User-Modell
from .models import Note, Category, MultiQuesModel, SingleQuestion, SingleChoiceQuestion, UserProfile, SingleChoiceOption, Answer
from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit


# Registration
class CustomUserCreationForm(UserCreationForm):
    preferred_language = forms.CharField(max_length=50, required=False, help_text="Ihre bevorzugte Programmiersprache")
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('preferred_language',)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise forms.ValidationError(
                "Nick must have be at least three signs. Der Benutzername muss mindestens 3 Zeichen lang sein."
            )
        return username



# Text question
class QuestionForm(forms.ModelForm):
    class Meta:
        model = SingleQuestion
        fields = ["question_text", "language_name", "question_type", "answer_text"]

    language_name = forms.ModelChoiceField(queryset=Category.objects.all())


# Multiple question form
# multiformular.html forms.py  class AddMultipleForm(forms.ModelForm): models.py class MultiQuesModel(models.Model): views.py class AddMultiQuestionView(View):
class AddMultipleForm(forms.ModelForm):
    ans_count = forms.IntegerField(min_value=1, label="Number of Answers Anzahl der Antworten")

    class Meta:
        model = MultiQuesModel
        fields = ["question", "language_name", "question_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ans_count = self.initial.get("ans_count", 1)
# ------------------------------------------------------------------------
        # This code allows to write to the database all correct answers
        """
        In summary, below code attempts to extract the value for ans_count from the form data and if an error occurs,
        it simply keeps the predefined value ans_count. This allows the value for ans_count to be taken from the form
        data if it is available, or to use the default value if it is unavailable or invalid.
        """
        if self.data is not None:
            try:
                ans_count=int(self.data.get('ans_count', ans_count))
            except ValueError:
                pass
# --------------------------------------------------------------------------
        for i in range(ans_count):
            self.fields[f"answer_{i}"] = forms.CharField(max_length=200, required=True)
            self.fields[f"is_correct_{i}"] = forms.BooleanField(
                required=False, widget=forms.CheckboxInput(attrs={"class": "checkbox"})
            )

    def clean(self):
        cleaned_data = super().clean()
        ans_count = cleaned_data.get("ans_count")
        print(ans_count)
        answers = []

        for i in range(ans_count):
            answer_text = cleaned_data.get(f"answer_{i}")
            is_correct = cleaned_data.get(f"is_correct_{i}")

            if answer_text:
                answers.append({"text": answer_text, "is_correct": is_correct})

        if not answers:
            raise forms.ValidationError(
                "Please fill out at least one answer. Bitte füllen Sie mindestens eine Antwort aus."
            )

        cleaned_data["answers"] = answers
        return cleaned_data


# Single choice Test
# ---------------------------------

class SingleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = SingleChoiceQuestion
        fields = ["question_text", "language_name", "question_type"]


    options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=False  # True makes an error
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["options"].choices = [(str(i), f"Option {i}") for i in range(1, 6)]

    def clean(self):
        cleaned_data = super().clean()
        selected_options = cleaned_data.get("options", [])

        return cleaned_data

        # if not selected_options or len(selected_options) != 1:
        #     raise forms.ValidationError(
        #         "Choose exactly one correct answer. Bitte wählen Sie genau eine richtige Antwort aus.")
        # if not selected_options:
        #     raise forms.ValidationError(
        #         "Please choose at least one answer. Bitte wählen Sie mindestens eine Antwort aus.")
        # if len(selected_options) != 1:
        #     raise forms.ValidationError("Choose exactly one correct answer. Bitte wählen Sie genau eine richtige Antwort aus.")



# For account tab
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["preferred_language"]
