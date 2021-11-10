import Calculate_func
from flask import Flask, render_template
from PIL import Image, ImageOps
import requests


app = Flask(__name__)

multiple_requests = {"IMAGE_FILE_NAME": {"min": "0", "max": "0", "mean": "0", "median": "0"}}

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/', methods=['GET'])
def HomePage():
    return render_template('home.html')

@app.route('/health', methods=['GET'])
def health():
    return render_template('health.html')


@app.route('/stats/<IMAGE_FILE_NAME>/<FUNC_NAME>', methods=['GET'])
def get_url(IMAGE_FILE_NAME, FUNC_NAME):
    URL = 'https://storage.googleapis.com/seetree-demo-open/{}'.format(IMAGE_FILE_NAME)
    if not is_url_image(URL):
        return render_template('image-file-name-404.html')
    if IMAGE_FILE_NAME in multiple_requests:
        if FUNC_NAME in multiple_requests[IMAGE_FILE_NAME]:
            return render_template('Calculate-function.html', FUNC_NAME=FUNC_NAME, IMAGE_FILE_NAME=IMAGE_FILE_NAME,
                                   value=multiple_requests[IMAGE_FILE_NAME][FUNC_NAME], url=URL)

    input_image = Image.open(requests.get(URL, stream=True).raw)
    gray_image = ImageOps.grayscale(input_image)

    if FUNC_NAME == 'max':
        max_value = Calculate_func.Max_value(gray_image)
        multiple_requests.update({IMAGE_FILE_NAME: {FUNC_NAME: max_value}})
        multiple_requests[IMAGE_FILE_NAME].update({FUNC_NAME: max_value})
        return render_template('Calculate-function.html', FUNC_NAME=FUNC_NAME, IMAGE_FILE_NAME=IMAGE_FILE_NAME, value=max_value, url=URL )

    elif FUNC_NAME == 'min':
        min_value = Calculate_func.Min_value(gray_image)
        multiple_requests.update({IMAGE_FILE_NAME: {FUNC_NAME: min_value}})
        multiple_requests[IMAGE_FILE_NAME].update({FUNC_NAME: min_value})
        return render_template('Calculate-function.html', FUNC_NAME=FUNC_NAME, IMAGE_FILE_NAME=IMAGE_FILE_NAME, value=min_value, url=URL)

    elif FUNC_NAME == 'mean':

        mean_value = Calculate_func.Mean_value(gray_image)
        multiple_requests.update({IMAGE_FILE_NAME: {FUNC_NAME: mean_value}})
        multiple_requests[IMAGE_FILE_NAME].update({FUNC_NAME: mean_value})
        return render_template('Calculate-function.html', FUNC_NAME=FUNC_NAME, IMAGE_FILE_NAME=IMAGE_FILE_NAME,value=mean_value,url=URL)

    elif FUNC_NAME == 'median':

        median_value = Calculate_func.Median_value(gray_image)
        multiple_requests.update({IMAGE_FILE_NAME: {FUNC_NAME: median_value}})
        multiple_requests[IMAGE_FILE_NAME].update({FUNC_NAME: median_value})
        return render_template('Calculate-function.html', FUNC_NAME=FUNC_NAME, IMAGE_FILE_NAME=IMAGE_FILE_NAME,value=median_value,url=URL)

    elif FUNC_NAME[0] == 'p' and FUNC_NAME[1:].isnumeric():
        if int(FUNC_NAME[1:]) >= 0 and int(FUNC_NAME[1:]) <= 100:
            percentile = Calculate_func.percentile_value(gray_image, int(FUNC_NAME[1:]))
            return render_template('Calculate-function.html', FUNC_NAME=FUNC_NAME, IMAGE_FILE_NAME=IMAGE_FILE_NAME, value=percentile,url=URL)

        else:
            return render_template('func--name-404.html')

    else:
        return render_template('func--name-404.html')




def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False


if __name__ == '__main__':
    app.run(host="0.0.0.0")