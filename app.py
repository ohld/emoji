import os
import requests

# from rq import Queue
# from rq.job import Job
# from worker import conn

import telegram
from flask import Flask, render_template, request, send_file

from imageGenerator import generate_random_emoji_cover

# q = Queue(connection=conn)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_to_channel(img_path):
    try:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(img_path, 'rb'))
    except:
        # TODO: fix with smth
        pass

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            # job = q.enqueue_call(
            #     func=generate_random_emoji_cover, result_ttl=5000
            # )
            # print(job.get_id())

            result_img_path = generate_random_emoji_cover()
            send_to_channel(result_img_path)
            return send_file(result_img_path, mimetype='image/gif')
        except Exception as e:
            errors.append(str(e) + 
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, results=results)

# @app.route("/results/<job_key>", methods=['GET'])
# def get_results(job_key):

#     job = Job.fetch(job_key, connection=conn)

#     if job.is_finished:
#         return send_file(job.result, mimetype='image/gif')
#         # return str(), 200
#     else:
#         return "Nay!", 202

if __name__ == '__main__':
    app.run()