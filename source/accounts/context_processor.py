from accounts.forms import LoginUserForm


def log_in_processor(request):
    if request.method == 'GET':
        form_log = LoginUserForm()
    elif request.method == 'POST':
        form_log = LoginUserForm(request.POST)
        if form_log.is_valid():
            pass
    else:
        form_log = None
        data = {
            'form_log': form_log,
        }
        return data
    if request.method == 'POST':
        return {}
