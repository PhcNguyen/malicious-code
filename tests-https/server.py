import sys
import os.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request
from lib.modules import (
    Terminal,
    GoogleSheet
)

app = Flask(__name__)
ID = '10rs_CfL4W5uKJI-ueX1n1MVZF4DT8uzqyb7wgtp0zfo'

@app.route('/', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        data = request.json
        GoogleSheet(ID).update_values([[data['key']]])
        return f"Received POST request with data: {data}"
    else:
        return "Only POST requests are allowed"


if __name__ == '__main__':
    Terminal().Clear()
    app.run(debug=True)
