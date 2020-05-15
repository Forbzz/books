import os
import uuid

import django
import pytest
from django.urls import reverse

if 'env setting':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryapp.settings')
    django.setup()

from django.test import TestCase

from book.apps import BookConfig
from book.models import Genre,Author,Book


@pytest.mark.django_db
def test_authors():

    authors = Author.objects.create(name='Харуки Минамото',age='58',description='Японский писатель', image='Den.jpg')
    authors.save()

    authors = Author.objects.create(name='Стивен Кинг', age='48', description='писатель', image='Den1.jpg')
    authors.save()

    authors = Author.objects.create(name='Дэн Браун', age='38', description='писатель', image='Den2.jpg')
    authors.save()

    assert Author.objects.count() == 3


@pytest.mark.parametrize('app',[BookConfig.name])
@pytest.mark.parametrize('expected', ['book'])
def test_app(app,expected):
    assert app == expected


@pytest.mark.django_db
def test_home_view(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_reg_view(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_activation_email(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.fixture()
@pytest.mark.django_db
def test_authors2():

    genre = Genre.objects.create(name='роман', url='url')
    genre.save()

    authors = Author.objects.create(name='Дэн Браун', age='38', description='писатель', image='Den2.jpg')
    authors.save()

    book = Book.objects.create(name='book',year='2020',genre=genre,author=authors,describe='describe',picture='smth.jpg')
    book.save()
    assert Book.objects.count() == 1


# @pytest.fixture
# @pytest.mark.django_db
# def test_auth_view(auto_login_user):
#     client, user = auto_login_user()
#     url = reverse('login')
#     response = client.get(url)
#     assert response.status_code == 200


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture()
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
