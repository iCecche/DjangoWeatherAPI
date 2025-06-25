from django.contrib.auth.views import LogoutView
from django.urls import path

from CustomUser.views import loginView, registerView, home, admin

urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home, name='home'),
    path('admin/', admin, name='admin'),
]