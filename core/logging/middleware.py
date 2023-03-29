import json, time
from datetime import datetime
from threading import local


thread_locals = local()


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        thread_locals.path =  request.path
        timestamp = time.monotonic()
        response = self.get_response(request)
        time_moment = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        data = {
            'request_total': round(time.monotonic() - timestamp, 3),
            'status_code': response.status_code,
            'path': request.path,
            'time_moment': time_moment,
        }

        with open('server/logging/request.log', 'a') as file:
            file.write(json.dumps(data) + '\n')

        thread_locals.path = ''

        return response
