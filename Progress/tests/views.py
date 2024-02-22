from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.forms import NewUserForm

class TestView(TemplateView):
    template_name = 'base.html'
    form_class = NewUserForm
    
    
