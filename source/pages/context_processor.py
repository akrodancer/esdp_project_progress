from pages.models import PageModel

def page_text_display(request):
    if request.method == 'GET':
        try:
            page = PageModel.objects.get(path=request.path)
            page_data = {
                'page': page
            }
            return page_data
        except:
            return {}
    return {}