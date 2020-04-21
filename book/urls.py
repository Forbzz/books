from django.urls import path
from django.views.generic import DetailView

from . import views
from libraryapp.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.contrib.auth import views as authViews


#DataFlair Django Tutorials
from .models import Book

urlpatterns = [
	path('', views.home, name = 'index'),
	path('upload/', views.upload, name = 'upload-book'),
	path('update/<int:book_id>', views.update_book),
	path('delete/<int:book_id>', views.delete_book),
	path('<int:pk>/', DetailView.as_view(model=Book, template_name='book/concrete_book.html'), name="book_detail"),
	path('review/<int:pk>/', views.AddReview.as_view(), name="add_review"),
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
]


if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)


'''x-html has doctype manadatory while html doesn't require you to declare doctype
xmlns type is mandatory in html
html, head, body and title is mandatory
must be properly nested
must be properly closed
must be used in lowercase

'''