from account.forms import LoginForm, RegisterForm
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import NotLoggedMixin
    

class LoginView(NotLoggedMixin, View):

    def post(self, request):
        login_form = LoginForm(request.POST)
        next = request.GET.get('next')
        if login_form.is_valid():
            fields = login_form.cleaned_data
            user = authenticate(request, username=fields['username'], password=fields['password'])
            if user:
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
        else:
            if next:
                return redirect('/account/login')
            else:
                return redirect('/account/login')

    def get(self, request):
        return render(request, 'login.html')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/account/login')
        else:
            return redirect('/')


class RegisterView(NotLoggedMixin, View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('/account/login/')
        else:
            return redirect('/account/register/')
