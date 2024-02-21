from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from accounts.models import User
from accounts.forms import NewUserForm
from typing import Any
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('homePage')


class UserRegisterView(CreateView):
    model = User
    template_name = 'accounts/sign_up.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('tests:test_page'))
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('tests:test_page')
        return next_url