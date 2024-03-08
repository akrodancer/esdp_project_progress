import json
from django.http import JsonResponse


class JsonFormHandler:
    def __init__(self, request, form) -> None:
        self.form = form
        self.request = request
        self.__status = 'none'

    def create_object(self):
        s = self.request.body.decode('utf-8')
        try:
            data = json.loads(s)
            print(s)
            print(self.form)
            form = self.form(data)
            if form.is_valid():
                form.save()
                self.__status = 'ok'
            else:
                self.__status = 'wrong_data'
        except:
            self.__status = 'error'
    
    def response(self):
        return JsonResponse({'result': self.__status})
        
    