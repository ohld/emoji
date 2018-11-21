import os
import requests

from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, send_file

from imageGenerator import generate_random_emoji_cover

q = Queue(connection=conn)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            result_img_path = generate_random_emoji_cover()
            print(result_img_path)
            return send_file(result_img_path, mimetype='image/gif')
        except Exception as e:
            errors.append(str(e) + 
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()