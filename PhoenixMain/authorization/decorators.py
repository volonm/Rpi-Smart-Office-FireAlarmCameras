from django.http import HttpResponse
from .models import SessionToken
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

SESSIONLIFE = timezone.timedelta(hours=6)
from sensors.models import Raspberry

def session_valid(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Extract the record identifier from the URL or request data, depending on your use case
        session_raw = request.headers.get('Session')
        token_raw = request.headers.get('Authorization')
        if session_raw and token_raw:
            received_token = str(token_raw).replace("Token ", "")
            received_session = str(session_raw).replace("Token ", "")

            time_now = timezone.now()
            time_valid = time_now - SESSIONLIFE
            # Check if the record exists in the database
            record = SessionToken.objects.get(session=received_session, created__gte=time_valid)
            # If session is correct
            if record:
                # If account token is correct
                uid = record.userID
                token_query = Token.objects.filter(user_id=uid)
                if token_query:
                    token_query.key = received_token
                    return view_func(request, *args, **kwargs)

            # Add your custom validity checks here, e.g., check if the record is valid
            if not record.is_valid:
                return HttpResponse("Record is not valid.", status=403)
        else:
            return Response({"detail": "Session and Token are required in headers"}, status=400)
        # If all checks pass, call the original view function

    return _wrapped_view


def only_rasps(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Extract the record identifier from the URL or request data, depending on your use case
        token_raw = request.headers.get('Authorization')
        if token_raw:
            received_token = str(token_raw).replace("Token ", "")
            # Check if the record exists in the database
            record = Raspberry.objects.get(token=received_token)
            if record:
                return view_func(request, *args, **kwargs)

        return HttpResponse("Record is not valid.", status=403)

    return _wrapped_view
