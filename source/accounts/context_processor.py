from accounts.forms import LoginUserForm


def log_in_processor(request):
    if request.method == 'GET':
            form_log = LoginUserForm(request.POST or None)

            data = {
                'form_log': form_log,
            }
            return data
    return {}
