from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Customer
from .forms import BookCreate, ReviewForm, SignUpForm, CreateUserForm
from django.http import HttpResponse


class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        return render(request, 'book/concrete_book.html,', {'book': book})


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.book = book
            form.save()
        return redirect('index')


def index(request):
    shelf = Book.objects.all()
    return render(request, 'book/library.html', {'shelf': shelf})


def upload(request):
    upload = BookCreate()
    if request.method == 'POST':
        upload = BookCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'book/upload_form.html', {'upload_form':upload})


def update_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('index')
    book_form = BookCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
        book_form.save()
        return redirect('index')
    return render(request, 'book/upload_form.html', {'upload_form':book_form})


def delete_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('index')
    book_sel.delete()
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.city = form.cleaned_data.get('city')
            user.save()
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ form : 'index'}}">reload</a>""")
    else:
        form = SignUpForm()
        return render(request, 'book/signup.html', {'form': form})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect ('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid ():
                form.save ()
                user = form.cleaned_data.get ('username')
                messages.success (request, 'Account was created for ' + user)
                return redirect ('login')

        context = {'form': form}
        return render (request, 'book/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect ('index')
    else:
        if request.method == 'POST':
            username = request.POST.get ('username')
            password = request.POST.get ('password')

            user = authenticate (request, username = username, password = password)

            if user is not None:
                login (request, user)
                return redirect ('index')
            else:
                messages.info (request, 'Username OR password is incorrect')

        context = {}
        return render (request, 'book/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def home(request):
    books = Book.objects.all()
    customers = Customer.objects.all()

    context = {'books':books, 'customers':customers}

    return render(request, 'book/main.html', context)
