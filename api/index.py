from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timedelta
import requests

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        server_key = 'AAAAAcZfmg4:APA91bFQJ53RqjpAJqoPIRxRTTTsNT4Ww-0cWGWJzuX7rDzvQcBihcwGCPIbFuZOGUSAWJDFVgNVmbf2Z-H3TC9p8IBBahd46Lt4-Sb8VHRcYwBg7JZbvXuvT6hMCyf5pFFwB0IxI0Eg'

        current_date = datetime.now().date()
        current_year = current_date.year
        holiday_file_path = f'holidays{current_year}.json'
        holidays = self.load_holidays(holiday_file_path)

        next_holiday = self.find_next_holiday(holidays)

        if next_holiday:
            holiday_name = next_holiday['name']
            holiday_date_str = next_holiday['date']['iso'].split('T')[0]  # Extract date part only
            holiday_date = datetime.strptime(holiday_date_str, '%Y-%m-%d').date()
            days_until_holiday = (holiday_date - current_date).days
            
            formatted_date = holiday_date.strftime('%d/%m/%Y')

            response_content = f"Next Holiday on {formatted_date} - {holiday_name}\n"
            if 0 < days_until_holiday <= 3:
                response_content += f"Upcoming Holiday on {formatted_date} - {holiday_name} in {days_until_holiday} days\n"
                self.send_notification(server_key, holiday_name, f"Will be in {days_until_holiday} days")
            else:
                response_content += "No Holidays with 3 days\n"
        else:
            response_content = "No upcoming holidays found.\n"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_content.encode('utf-8'))

    def load_holidays(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data['response']['holidays']

    def send_notification(self, server_key, title, body):
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': 'key=' + server_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'notification': {
                'title': title,
                'body': body
            },
            'to': '/topics/all' 
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"Notification sent: {response.status_code}, {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")

    def find_next_holiday(self, holidays):
        current_date = datetime.now().date()
        next_holiday = None
        for holiday in holidays:
            try:
                holiday_date_str = holiday['date']['iso'].split('T')[0]  # Extract date part only
                holiday_date = datetime.strptime(holiday_date_str, '%Y-%m-%d').date()
                if holiday_date > current_date:
                    next_holiday = holiday
                    break
            except ValueError as e:
                print(f"Error parsing holiday date: {e}")
        return next_holiday
