from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.dynamic_form, name='generatedAi'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('thanks/', views.thanks, name='thanks'),
    path('login/', views.login_page, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]