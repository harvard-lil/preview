from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from PIL import Image

import random, string, subprocess, os, json, re, urllib


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
    url = urllib.unquote(url)
    viewport = request.GET.get('viewport', None)
    thumbnail= request.GET.get('thumb', None)

    # Get a unique identifier
    get_id = lambda: ''.join([random.choice(string.ascii_letters) for n in xrange(8)])
    file_name = '%s.png' % get_id()
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Send our phantomjs png creation command out through a subprocess
    image_generation_command = settings.BASE_DIR + \
                               '/lib/phantomjs ' + \
                               '--ignore-ssl-errors=yes --ssl-protocol=any ' + \
                               settings.BASE_DIR + '/lib/rasterize.js "' + \
                               url + '" ' + file_path

    if viewport:
        image_generation_command += ' "' + viewport + '"'

    subprocess.call(image_generation_command, shell=True)

    # The thing we send the user
    json_resonse = {'image_url': os.path.join(settings.MEDIA_URL, file_name)}


    # If we get a thumbnail parameters, resize the image
    if thumbnail:
        m = re.search(r"^([0-9]+)px\**([0-9]*)", thumbnail)
        requested_thumb_width = int(m.group(1))

        thumb_name = "thumb-" + file_name
        thumb_path = os.path.join(settings.MEDIA_ROOT, thumb_name)
        im = Image.open(file_path)


        # If the user doesn't specify a height for the thumb, let's
        # use the existing height of the image (ratio adjusted against width)
        wpercent = (requested_thumb_width/float(im.size[0]))
        h_size = int((float(im.size[1])*float(wpercent)))
        size = (requested_thumb_width, h_size)
        thumb = im.resize(size, Image.ANTIALIAS)

        # If the user does specify a height, let's crop that thing down
        if m.group(2):
            h_size = int(m.group(2))
            thumb = thumb.crop((0,0, requested_thumb_width, h_size))

        thumb.save(thumb_path)

        json_resonse['thumb_url'] = os.path.join(settings.MEDIA_URL, thumb_name)

    return HttpResponse(json.dumps(json_resonse), mimetype="application/json")
