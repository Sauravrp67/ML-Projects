from wsgiref.simple_server import make_server

# Define a WSGI application
def simple_app(environ, start_response):
    # Define the HTTP response status and headers
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    # Call the start_response function with the status and headers
    start_response(status, headers)

    # Return the response body as an iterable (list of strings)
    return [b"Hello, World! This is a WSGI application."]

# Create a WSGI server using make_server
server = make_server('localhost', 8000, simple_app)
print("Server running on port 8000...")

# Start the server and serve requests indefinitely
server.serve_forever()
