import argparse
import requests
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pdfkit
from dateutil.parser import parse

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

    TEMPLATE_FILE = "template.html"
    template = env.get_template(TEMPLATE_FILE)

    output = template.render(user_details=user_details, memories=memories)
    print(user_details)
    
    user_id = user_details['_id']

    html_file = open(f'./output/html/{user_id}.html', 'w')
    html_file.write(output)
    html_file.close()

    pdfkit.from_file(f'./output/html/{user_id}.html', f'./output/pdf/{user_id}.pdf')

    return user_id

if __name__=="__main__":
    main()




