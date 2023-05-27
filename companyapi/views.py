import json
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View


def get_google_calendar_credentials():
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    redirect_uri = settings.REDIRECT_URI

    return client_id, client_secret, redirect_uri

# class based View
# Endpoint: /rest/v1/calendar/init/
class GoogleCalendarInitView(View):
    def get(self, request):
        client_id, client_secret, redirect_uri = get_google_calendar_credentials()
        # Step 1: Redirect the user to Google's OAuth consent screen
        auth_url = f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=https://www.googleapis.com/auth/calendar.readonly'
        return HttpResponseRedirect(auth_url)


# Endpoint: /rest/v1/calendar/redirect/
class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Step 2: Exchange the authorization code for an access token
        code = request.GET.get('code')

        token_url = 'https://accounts.google.com/o/oauth2/token'

        token_payload = {
            'code': code,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'redirect_uri': settings.REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        # Send a POST request with data (=token_payload)
        token_response = requests.post(token_url, data=token_payload)
        # Parse the response JSON data
        token_data = json.loads(token_response.text)

        #obtaining the access token from the OAuth flow
        access_token = token_data.get('access_token')

    # Step 3: Use the access token to get a list of events in the user's calendar

        # Set the API endpoint URL for fetching events from the user's primary calendar
        events_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'

        # Set the headers with the access token for authentication
        headers = {'Authorization': f'Bearer {access_token}'}

        # Send a GET request to retrieve the events
        events_response = requests.get(events_url, headers=headers)
        # Parse the response JSON data
        events_data = json.loads(events_response.text)

        # here we can use event_data as per our requirement.....

        return HttpResponse('Events retrieved successfully')

