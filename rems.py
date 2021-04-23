import argparse
import requests
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pdfkit
from dateutil.parser import parse
import base64

base_url = "https://rembook.nitt.edu/api/"
login = "login"
my_memories = "memory/getMyMemories"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="Enter your email")
    parser.add_argument("password", help="Enter your password")
    args = parser.parse_args()

    email = args.email
    password = args.password

    user_details = get_user_details(email, password)

    memories = get_memories(user_details)

    user_id = get_rem(user_details, memories)

def get_user_details(email, password):

    login_request = requests.post(
        base_url + login,
        data = {
            "email": email,
            "password": password
        }
    )

    return login_request.json()

def get_memories(user_details):

    if user_details['dob']:
        user_details['dob'] = parse(user_details['dob'])
        user_details['dob'] = user_details['dob'].date()
    
    memory_request = requests.post(
        base_url + my_memories,
        data = {
            "session": user_details["session"]
        }
    )

    return memory_request.json()


def get_rem(user_details, memories):
    env = Environment(
        loader = FileSystemLoader(searchpath="./templates/"),
        autoescape = select_autoescape(['html', 'xml'])
    )

    TEMPLATE_FILE = "template_modified.html"
    template = env.get_template(TEMPLATE_FILE)

    output = template.render(user_details=user_details, memories=memories)
        
    user_id = user_details['_id']

    html_file = open('./output/html/' + user_id + '.html', 'w')
    html_file.write(output)
    html_file.close()

    pdfkit.from_file('./output/html/' + user_id + '.html', './output/pdf/' + user_id + '.pdf')
    return user_id

def get_b64_rem(user_details, memories):
    env = Environment(
        loader = FileSystemLoader(searchpath="./templates/"),
        autoescape = select_autoescape(['html', 'xml'])
    )
    TEMPLATE_FILE = "template_modified.html"
    template = env.get_template(TEMPLATE_FILE)

    output = template.render(user_details=user_details, memories=memories)
    
    user_id = user_details['_id']

    html_file = open('./output/html/' + user_id + '.html', 'w')
    html_file.write(output)
    html_file.close()

    pdfkit.from_file('./output/html/' + user_id + '.html', './output/pdf/' + user_id + '.pdf')
    with open('./output/pdf/' + user_id + '.pdf', "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())

    return encoded_string

if __name__=="__main__":
    main()




