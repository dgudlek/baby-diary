# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import request
import gspread
import random
import math
import datetime
import pytz
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import datastore
import command_handler

# Instantiates a client
datastore_client = datastore.Client()

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')

def get_state():
    return datastore_client.get(datastore_client.key("state", token))

def update_state(state):
    return datastore_client.put(state)

def log_in_spreadsheet(row):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sh = client.open_by_url(
        'https://docs.google.com/spreadsheets/d/1BChungVqS1ovKjjd8vY4dl2Ko01yAIdxNGph44UWAFo/edit#gid=0'
    )

    # Extract and print all of the values
    return sh.values_append(
        'data!A1:A',
        params={
            'valueInputOption': 'USER_ENTERED'
        },

        body={
            'values': [row]
        }
    )

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def describe_state(state):
    if "start" not in state:
        return ""
    else:
        message = "<pre>Timer started %d min ago (%s) on %s side<br/>voice: '%s'</pre>" % (
                math.floor((datetime.datetime.now(pytz.UTC) - state["start"]).seconds / 60),
                state["start"].astimezone(pytz.timezone('Europe/Zagreb')).strftime("%H:%M"),
                state["side"],
                state["start_query"],
            )
        return "<div style='padding-top: 5px; padding-left: 20px;'>\n%s\n</div>" % message


@app.route('/status', methods=['GET'])
def handle_status():
    # the div with 500px and hidden overflow is used to crop the
    # footer that google sheets install
    message = """
    <html>
    <head>
        <style>
            body { margin:0; }
            iframe {
                width: 100%%
            }
        </style>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="60">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    </head>
    <body>
        %s
        <div style='height: 500px; overflow:hidden;'><iframe
            frameBorder=0px
            width=100%%
            height=600px
            src="%s&cachemiss=%d">
        </iframe></div>
    </body>
    </html>
    """ % (
        describe_state(get_state()),
        "https://docs.google.com/spreadsheets/d/1BChungVqS1ovKjjd8vY4dl2Ko01yAIdxNGph44UWAFo/htmlembed#gid=129832092",
        random.randint(1,1000000),
    )
    return message

@app.route('/ifttt', methods=['GET', 'POST'])
def handle_ifttt():
    """Return a friendly HTTP greeting."""
    # TODO dora: proictaj upit iz URL parametra 'q'
    # napisi klasu SpreadsheetProxy
    # napisi klasu LogRequestParser
    # i iz ove funkcije pospoji te dvije klase da naprave sto trebaju.
    if not app.debug and request.method == 'GET':
        return "Method not alowed", 405

    if not request.args.get('token') == token:
        print ("Token is bad")
        return "Token is bad"

    q = request.args.get('q')
    if app.debug and q is not None:
        q += " for testing"

    state = get_state()
    message, row = command_handler.parse(q, state)
    update_state(state)

    if row is not None:
        log_in_spreadsheet(row)

    message += "<br>"
    message += describe_state(state)
    print(message)
    return message


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
