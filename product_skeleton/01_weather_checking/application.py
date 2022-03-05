import datetime
from flask import Flask
from flask import render_template, render_template_string, redirect
import boto3
import time
import requests
import json
import os

from user_definition import *

application = Flask(__name__)


def read_s3_obj(bucket_name, output_file):
    """ Read from s3 bucket"""
    try:
        session = boto3.Session(
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
        s3 = session.resource('s3')
        obj = s3.Object(bucket_name, output_file)
        body = obj.get()['Body'].read().decode('utf-8')
        return body
    except KeyError:
        return ""


def retreive_web_data():
    api_key = os.environ['API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}" \
          f"&zip={zip},us&units=imperial"
    response = requests.get(url)
    x = response.json()
    main = x['weather'][0]['main']
    temp = x['main']['temp']
    return main, temp


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    """ index page -- shown on the beginning """
    body = read_s3_obj(bucket_name, output_file)

    return render_template('index.html', output=body)


@application.route('/calculate', methods=['GET', 'POST'])
def calculate():
    """ Read OpenWeatherMap API"""
    main, temp = retreive_web_data()

    if (main in ['Clear', 'Clouds'] and 60 < temp < 85):
        msg = "Go for a walk"
    else:
        msg = "Stay home"
    prev_reading = read_s3_obj(bucket_name, output_file)
    
    body = "{}\t{}\t{}\t{}\t{}\n\n".format(msg,
                                         datetime.datetime.now(),
                                         main,
                                         temp,
                                         prev_reading)

    boto3.resource("s3")\
         .Bucket(bucket_name)\
         .put_object(Key=output_file, Body=body, ACL='public-read-write')

    return redirect("/index")


if __name__ == '__main__':
    application.jinja_env.auto_reload = True
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.run(host='0.0.0.0', port=80, debug=True)
