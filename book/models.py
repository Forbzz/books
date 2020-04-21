from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
	name = models.CharField(verbose_name="Название",max_length = 50)
	year = models.PositiveSmallIntegerField("Год издания",default = 0)
	picture = models.ImageField(verbose_name="Обложка")
	author = models.ManyToManyField(Author, verbose_name = "автор", related_name = "book_author")
	genre = models.ManyToManyField(Genre, verbose_name = "жанры")
	describe = models.TextField(default = 'Описание книги')
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
		return self.name

	class Meta:
		verbose_name = "Отзыв"
		verbose_name_plural = "Отзывы"


class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Пользователь"
		verbose_name_plural="Пользователи"

