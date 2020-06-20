import os

from flask import Flask, request, jsonify, make_response, send_file, render_template

from rems import get_user_details, get_memories, get_rem

app = Flask(__name__)

@app.route('/', methods=['GET'])
def rem_form():
    error = request.args.get('error', None)
    return render_template('index.html', error=error)

@app.route('/generate', methods=['POST'])
def generate():
    # Check if request is proper
    if not request.form or \
        'email' not in request.form or \
        'password' not in request.form:
        return render_template('index.html', error='Bad Request')

    email = request.form['email']
    password = request.form['password']

    # Login user
    user_details = get_user_details(email, password)
    user_details_response = user_details.get('message', 'SUCCESS')
    if user_details_response == 'User not found' or \
        user_details_response == 'Webmail Credentials Invalid':
        return render_template('index.html', error='User not found')

    # Get memories
    memories = get_memories(user_details)

    # Generate pdf
    user_id = get_rem(user_details, memories)
    
    # Send pdf
    return send_file(os.getcwd() + f'/output/pdf/{user_id}.pdf')