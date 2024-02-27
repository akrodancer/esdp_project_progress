from site_pages.models import PageFlatText

def page_text_display(request):
    if request.method == 'GET':
        try:
            page = PageFlatText.objects.get(path=request.path)
            page_data = {
                'page': page
            }
            return page_data
        except:
            return {}
    return {}