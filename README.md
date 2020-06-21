# SaveRems

## Setup

1. Clone the repository
`https://github.com/surajk16/SaveRems `

2. Install the requirements
`pip3 install -r requirements.txt`

3. Create Output Directory
`mkdir output && mkdir output/html && mkdir output/pdf`

4. Install [wkhtmltopdf](https://wkhtmltopdf.org/)

5. Run the flask webserver
```
export FLASK_APP=web.py
flask run
```

6. Run the python script by passing in your webmail/email and password as params.
`python3 rems.py sample@gmail.com password`

7. To autorun script on changes to _rems.py_ and  _template.html_, install [inotifywait](https://github.com/inotify-tools/inotify-tools/wiki) and run the command
`while inotifywait -e close_write template/template.html; do python3 rems.py sample@gmail.com password; done` and
`while inotifywait -e close_write rems.py; do python3 rems.py sample@gmail.com password; done` from the working directory.

8. Find the output html and pdf in the output folder.
