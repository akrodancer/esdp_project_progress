from accounts.forms import LoginUserForm


def log_in_processor(request):
    if request.method == 'GET':
        try:
            form_log = LoginUserForm()

            data = {
                'form_log': form_log,
            }
        except:
            return {}
    return {}

