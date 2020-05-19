from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Customer, User, Profile
from .forms import BookCreate, ReviewForm, SignUpForm, CreateUserForm, UserRegistrationForm
from django.http import HttpResponse
import logging
from .tokens import account_activation_token

# logger = logging.getLogger('book.views.activate')

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


@login_required(login_url="/login")
def upload(request):
    logger = logging.getLogger('django')
    upload = BookCreate()
    if request.method == 'POST':
        upload = BookCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            logger.info(f"Book has been successfully added to shelf")
            return redirect('index')
        else:
            logger.warning("smth wrong with adding a book")
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'book/upload_form.html', {'upload_form':upload})


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def delete_book(request, book_id):
    logger = logging.getLogger('django')
    book_id = int(book_id)
    try:
        book_sel = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('index')
    book_sel.delete()
    logger.info(f"book with id={book_id} has been deleted")
    return redirect('index')

def signup(request):
    logger = logging.getLogger('django')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.city = form.cleaned_data.get('city')
            user.save()
            login(request, user)
            logger.info(f"{user.username} successfully authorized to site")
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ form : 'index'}}">reload</a>""")
    else:
        form = SignUpForm()
        return render(request, 'book/signup.html', {'form': form})


def loginPage(request):
    logger = logging.getLogger('django')
    if request.user.is_authenticated:
        return redirect ('index')
    else:
        if request.method == 'POST':
            username = request.POST.get ('username')
            password = request.POST.get ('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login (request, user)
                logger.info(f"{username} successfully authorized to site")
                return redirect('index')
            else:
                logger.warning(f"incorrect username or password by {username}")
                messages.info(request, 'Неверное имя пользователя или пароль')

        context = {}
        return render(request, 'book/login.html', context)


def activate(request, uidb64, token):
    logger = logging.getLogger('django')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        logger.error('Once of error excepted: TypeError, ValueError, OverflowError, User.DoesNotExist')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        logger.info(f'verified successfully for {user.username}')
        return render(request, 'book/activate.html')
    else:
        logger.warning("verified isn't successfully")
        return HttpResponse('Activation link is invalid!')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect ('index')
    else:
        logger = logging.getLogger('django')

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid ():
                userValue = form.cleaned_data.get ("username")
                email = form.cleaned_data.get ("email")
                password1Value = form.cleaned_data.get ("password1")
                password2Value = form.cleaned_data.get ("password2")

                user = User.objects.create_user (username = userValue, email = email, password = password2Value)
                user.is_active = False
                user.save ()
                current_site = get_current_site (request)
                mail_subject = 'Активация аккаунта.'
                token = account_activation_token.make_token (user)

                message = render_to_string ('book/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                })
                to_email = form.cleaned_data.get ('email')
                email = EmailMessage (
                    mail_subject, message, to = [to_email]
                )
                email.send()
                messages.info(request, 'Письмо с завершением авторизации отправлено на вашу почту')

                logger.info(f'Email send to {userValue}')
                return redirect ('login')
        context = {'form': form}
        return render(request, 'book/register.html', context)





def logoutUser(request):
    logout(request)
    return redirect('index')


def home(request):
    books = Book.objects.all()
    customers = Customer.objects.all()

    context = {'books':books, 'customers':customers}

    return render(request, 'book/main.html', context)
