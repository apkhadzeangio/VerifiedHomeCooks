from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomerRegistrationForm, UserLoginForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('dashboard:role_redirect')


class UserLogoutView(LogoutView):
    pass


def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:customer_dashboard')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
