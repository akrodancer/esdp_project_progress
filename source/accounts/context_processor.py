from accounts.forms import NewUserForm, LoginUserForm
from django.contrib.auth import login, authenticate



def log_in_processor(request):
    if request.method == 'GET':
            form_log = LoginUserForm(request.POST or None)

            data = {
                'form_log' : form_log,
            }
            return data
