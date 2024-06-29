from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        current_datetime = datetime.now()

        # Extract each component
        day = current_datetime.day
        month = current_datetime.month
        year = current_datetime.year
        hour = current_datetime.hour
        minute = current_datetime.minute

        # Create the response content
        response_content = f"""
        Current Date and Time: {current_datetime}
        Day: {day}
        Month: {month}
        Year: {year}
        Hour: {hour}
        Minute: {minute}
        """

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_content.encode('utf-8'))
        return
