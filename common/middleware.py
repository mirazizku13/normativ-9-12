import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

class LoginIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', 'Noma\'lum IP')
        now = datetime.datetime.now()
        # print(f"now: [{now}] So'rov IP {ip}")
        # print(f'ip: {ip}')
        response = self.get_response(request)
        return response


class TimeLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now()
        if not (9 <= now.hour <= 21):
            return render(request,'time_limit.html')
        response = self.get_response(request)
        return response

iplists = {}
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        now = datetime.datetime.now()

        if ip not in iplists:
            iplists[ip] = []

        iplists[ip] = [
            request_time
            for request_time in iplists[ip]
            if (now - request_time).total_seconds() < 10

        ]

        iplists[ip].append(now)
        # print(iplists)

        if len(iplists[ip]) > 10:
            return HttpResponse('Rate limit exceeded')

        response = self.get_response(request)
        return response

class UserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', 'Noma\'lum brouzer')
        # print(f'brauzer nomi: {user_agent}')

        response = self.get_response(request)
        return response
