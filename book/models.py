from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, User
from multiprocessing.pool import ThreadPool
from django.db.models.signals import post_save
from django.dispatch import receiver


# class User(AbstractUser):
# 	email = models.EmailField(unique = True)

class Author(models.Model):
    name = models.CharField("Имя", max_length = 100)
    age = models.PositiveSmallIntegerField("Возраст", default = 0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to = "media/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Автор"
        verbose_name_plural="Авторы"


class Genre(models.Model):
    name = models.CharField("Имя", max_length = 100)
    url = models.SlugField(max_length = 100, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"


class Book(models.Model):
    name = models.CharField("Название",max_length = 50)
    year = models.PositiveSmallIntegerField("Год издания",default = 0)
    picture = models.ImageField()
    author = models.ManyToManyField(Author, verbose_name = "автор", related_name = "book_author")
    genre = models.ManyToManyField(Genre, verbose_name = "жанры")
    describe = models.TextField("Описание",default = 'Описание книги')
    url = str(id)

    def __str__(self):
        return self.name

    def get_absolute_url (self):
        return reverse("movie_detail", kwargs = {"slug": self.url})

    class Meta:
        verbose_name="Книга"
        verbose_name_plural="Книги"


class Reviews(models.Model):

    name = models.CharField("Имя пользователя", max_length = 100)
    text = models.TextField("Отзыв", max_length = 1000)
    parent = models.ForeignKey(
        'self', verbose_name = "Родитель", on_delete = models.SET_NULL, blank = True, null = True
    )
    book = models.ForeignKey(Book, verbose_name = "книга", on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.book.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + "_" + str(self.Verified)

    class Meta:
        verbose_name = "Авторизованные пользователи"
        verbose_name_plural = "Авторизованные пользователи"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_active is True:
            instance.profile.Verified = True
        else:
            instance.profile.Verified = False
        instance.profile.save()



class Mail(models.Model):
    topic = models.CharField(max_length=120)
    text = models.TextField()
    date = models.DateField("date")
    time = models.TimeField()
    users = models.ManyToManyField(Profile, limit_choices_to={'Verified': True}, blank=False)
    check_send = models.BooleanField(default=False)

    def __str__(self):
        if self.check_send is False:
            self.check_send = True
            self.send()
            self.save()
        return str(self.topic)

    def send(self):
        message = render_to_string('accounts/acc_active_email.html', {
            'text': self.text,
            'date': self.date,
            'time': self.time
        })
        mail_subject = self.topic
        mount = self.users.count()
        pool_executor = ThreadPool(mount)
        result = []
        for profile in self.users.all():
            to_email = profile.user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email])
            result.append(email)

        pool_executor.map(send_mail, result)


def send_mail(email):
    email.send()

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)
#
# 	instance.profile.save()

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
