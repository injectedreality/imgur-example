import hashlib
from io import BytesIO

import flask
from flask import Response
from flask.app import request
from google.cloud import storage
from google.cloud.storage import Client
from PIL import Image

"""
a REST API to upload a picture(returns an identifier of the uploaded picture)
a REST API to get a picture(an identifier of the picture is provided)
a distributed backend(a pool of workers can retrieve at any time any uploaded picture)
workers should be running in an IaaS of your choice

An unordered list of bonuses: 
Bonus A - optional size parameter when getting a picture, you can specify preferred size: low, medium, high, original 
Bonus B - elastic pool - spawn new workers and delete them automatically based on usage
Bonus C - a smart way of handling netsplits between geo locations
Bonus D - any kind of optimization of your backend's backing store(detect identical files, lazy sharing between workers based on geo locations, whatever you feel like really…)
"""

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['BUCKET_NAME'] = 'pexip-demo-files'


@app.route('/', methods=['GET'])
def documentation():
    return "POST raw image data to /api/v1/images"


@app.route('/api/v1/images', methods=['POST'])
def add_images():
    checksum = hashlib.md5(request.data).hexdigest()
    extension = request.headers.get('Content-Type').split('/')[1]

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(app.config.get('BUCKET_NAME'))
    blob = bucket.blob(f'{checksum}/original.{extension}')
    blob.upload_from_file(file_obj=BytesIO(request.data))

    return Response(f'{checksum}.{extension}')


@app.route('/api/v1/images/<string:image_name>',  defaults={'size': 'original'}, methods=['GET'])
@app.route('/api/v1/images/<string:size>/<image_name>')
def get_image(image_name, size='original'):
    storage_client = Client.from_service_account_json('./storage-credentials.json')
    #storage_client = storage.Client()
    bucket = storage_client.get_bucket(app.config.get('BUCKET_NAME'))
    checksum, extension = image_name.split('.')
    blob = bucket.blob(f'{checksum}/original.{extension}')
    file_obj = BytesIO()
    blob.download_to_file(file_obj=file_obj)
    file_obj.seek(0)

    if size != 'original':
        im = Image.open(file_obj)
        width = 100
        height = 100
        if size == 'low':
            (width, height) = (im.width / 3, im.height / 3)
        elif size == 'medium':
            (width, height) = (im.width / 2, im.height / 2)
        elif size == 'high':
            (width, height) = (im.width * 2, im.height * 2)

        im_resized = im.resize((int(width), int(height)))
        file_obj = BytesIO()
        im_resized.save(file_obj, 'jpeg')
        file_obj.seek(0)
        print("Hello world")

    # original

    return Response(file_obj.read(), content_type=f'image/{extension}')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')