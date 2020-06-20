import argparse
import requests
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pdfkit

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

    login_request = requests.post(
        base_url + login,
        data = {
            "email": email,
            "password": password
        }
    )

    user_details = login_request.json()

    memory_request = requests.post(
        base_url + my_memories,
        data = {
            "session": user_details["session"]
        }
    )

    memories = memory_request.json()

    renderTemplate(user_details, memories)


def renderTemplate(user_details, memories):
    env = Environment(
        loader = FileSystemLoader(searchpath="./template/"),
        autoescape = select_autoescape(['html', 'xml'])
    )

    TEMPLATE_FILE = "template.html"
    template = env.get_template(TEMPLATE_FILE)

    output = template.render(user_details=user_details, memories=memories)

    html_file = open('./output/my_rem.html', 'w')
    html_file.write(output)
    html_file.close()

    pdfkit.from_file('./output/my_rem.html', './output/my_rem.pdf')

if __name__=="__main__":
    main()




