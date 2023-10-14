import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from ..models import UserProfile
from ..forms import CustomUserCreationForm
from django.test import Client
User = get_user_model()
CustomUser = get_user_model()


@pytest.fixture
def client():
    # Erstellen Sie einen Testclient
    return Client()

@pytest.fixture
def user_data():
    # Erstellen Sie hier die notwendigen Benutzerdaten, die Sie in Ihrem Test verwenden möchten
    return {
        'username': 'testuser',
        'password': 'testpassword',
        # Weitere Felder, die Sie benötigen
    }
@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
    return user

@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

# Falls Sie ein benutzerdefiniertes Benutzermodell verwenden, passen Sie den Import und die Verwendung an
@pytest.fixture
def custom_staff_user(db):
    user = CustomUser.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
    return user

@pytest.fixture
def custom_regular_user(db):
    user = CustomUser.objects.create_user(username='testuser', password='testpassword')
    return user




