from django.shortcuts import render
from django.views.generic import TemplateView, View
from accounts.forms import NewUserForm, LoginUserForm

class TestView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'base.html'
        login_form = LoginUserForm
        context = {
            'login_form': login_form
            }

        return render(request, template_name, context)
    
    
