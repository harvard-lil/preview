from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

import random, string, subprocess, os, json


def landing(request):
    """
    Our landing page. Pitch the project and describe to use it.
    """
    return render_to_response('landing.html')

def generate_preview(request):
    """
    Receive a URL as a parameter and possibly some flags on how
    to render the image. Create a png thumbnail of the url
    and return the path in a json object.
    """

    url = request.GET.get('url')
    slice_size = request.GET.get('slice-size', None)

    # Get a unique identifier
    get_id = lambda: ''.join([random.choice(string.ascii_letters) for n in xrange(8)])
    file_name = '%s.png' % get_id()

    # Send our phantomjs png creation command out through a subprocess
    image_generation_command = settings.BASE_DIR + '/lib/phantomjs ' + \
                               settings.BASE_DIR + '/lib/rasterize.js "' + \
                               url + '" ' + \
                               os.path.join(settings.MEDIA_ROOT, file_name)



    if slice_size:
        image_generation_command += ' "' + slice_size + '"'

    subprocess.call(image_generation_command, shell=True)

    json_resonse = {'image_url': os.path.join(settings.MEDIA_URL, file_name)}

    return HttpResponse(json.dumps(json_resonse), mimetype="application/json")
