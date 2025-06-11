import time as time_module
import logging
from django.http import HttpResponseForbidden
from datetime import datetime, time


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        allowed_start = time(0, 0)
        allowed_end = time(23, 0)
        if not (allowed_start <= now <= allowed_end):
            return HttpResponseForbidden(f"Chat access is only allowed between {allowed_start} and {allowed_end}.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.endswith('/messages/'):
            ip = self.get_client_ip(request)
            now = time_module.time()

            # Initialize or filter old entries
            timestamps = self.message_log.get(ip, [])
            # keep only last 60s
            timestamps = [t for t in timestamps if now - t < 60]

            if len(timestamps) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            timestamps.append(now)
            self.message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
