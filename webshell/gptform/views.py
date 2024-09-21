from django.shortcuts import render, redirect
from .forms import generate_form_from_csv
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def dynamic_form(request):
    form = generate_form_from_csv('gptform/static/docConfig.xlsx')
    return render(request, 'dynamic-form.html', {'form': form})

@login_required
def contact_us(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # send_mail(
        #     subject=f"Contact form submission from {name} : {email}",
        #     message=message,
        #     from_email="MKC-AI@mkcconsultants.com.au",
        #     recipient_list=["daniel.brighton@mkcconsultants.com.au"],
        #     fail_silently=False
        # )

        return redirect('thanks')
    else:
        return render(request, 'contact-us.html')

@login_required
def thanks(request):
    return render(request, "thanks.html")


def login_page(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_to = request.POST.get('next', request.GET.get('next', ''))
            if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts={request.get_host()}):
                redirect_to = settings.LOGIN_REDIRECT_URL
            return redirect(redirect_to)
        else:
            context['error'] = "Invalid username or password"
    return render(request, 'login.html', context)