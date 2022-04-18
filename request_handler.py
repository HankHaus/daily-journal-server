from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from views import get_all_entries, get_single_entry, delete_entry, get_entries_by_search
from views import get_all_moods

class HandleRequests(BaseHTTPRequestHandler):

    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

# Q: can you walk me through this function? i have no clue what's going on in it
    def parse_url(self, path):
        """_summary_

        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """

# Q:this function is for setting the headers to the appropriate codes in the other functions, right?
# A:y
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def do_OPTIONS(self):
        """Sets the options headers
        """
        # Q: what is the point of this function? I don't know that i've messed around with the http options verb before
        # A:this tells the browser what requests the server allows and doesn't allow, for instance this allows
        # get post put and delete

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


    def do_GET(self):
        """_summary_
        """
        # Q: sets the code on the response as 200 success
        self._set_headers(200)

# Q:initializes the response as an empty dictionary so we can add things to it
# A:y
        response = {}

        # Q: what does this line do?
        # A:
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`

        # Q: does this say "if the length of the parsed url is 2 after being split on '/'
        # then we will say the the url was resource/id"
        # then it narrows down which function to run based off the resource and wether or not the id exists.
        
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_moods()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "q" and resource == "entries":
                response = get_entries_by_search(value)

            elif key == "location_id" and resource == "animals":
                response = get_animals_by_location(value)

            elif key == "location_id" and resource == "employees":
                response = get_employees_by_location(value)

            elif key == "status" and resource == "animals":
                response = get_animals_by_status(value)

        self.wfile.write(f"{response}".encode())

    def do_POST(self):
        """_summary_
        """
        # Q: what is rfile?
        # A: rfile is inherited from basHTTPrequesthandler 
        # allows you to reach into request and pull out the body of it
        # Q:what is int()?
        # A: works the same as parseInt()
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        # Q:why do we have an index at the end of this line?
        # A: parse url returns a tuple, only care about the resource, don't care about the index rn
        resource = self.parse_url(self.path)[0]

        # Initialize new animal
        new_animal = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)

        # Encode the new animal and send in response
        # Q: what is .encode() doing?
        # A: encode enables us to send the new_animal fstring back to the client
        self.wfile.write(f"{new_animal}".encode())

        new_employee = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "employees":
            new_employee = create_employee(post_body)

        # Encode the new animal and send in response
        # Q: what is wfile?
        # A: part of converting it to be able to send to the client
        self.wfile.write(f"{new_employee}".encode())

        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "customers":
            new_customer = create_customer(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_customer}".encode())

    def do_PUT(self):
        """_summary_
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())


    def do_DELETE(self):
        """_summary_
        """
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)

        if resource == "locations":
            delete_location(id)

        if resource == "employees":
            delete_employee(id)

        if resource == "customers":
            delete_customer(id)
    # Encode the new animal and send in response
        self.wfile.write("".encode())



def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

# Q:what is this checking? it's an if statement ouside of a function, so i'm not sure what __name__ comes from
# A:
if __name__ == "__main__":
    main()
