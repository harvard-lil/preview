from django.http import HttpResponse
import random, string, subprocess, os, json
from django.conf import settings

def generate_preview(request):
    url = request.GET.get('url')

    #accept a url
    #generate id for
    #put phantom on the job
    #put phantom's contents in a media dir

    # Get a unique identifier
    get_id = lambda: ''.join([random.choice(string.ascii_letters) for n in xrange(8)])
    file_name = '%s.png' % get_id()

    # Send our phantomjs png creation command out through a subprocess
    image_generation_command = settings.BASE_DIR + '/lib/phantomjs ' + \
                               settings.BASE_DIR + '/lib/rasterize.js "' + \
                               url + '" ' + \
                               os.path.join(settings.MEDIA_ROOT, file_name) + \
                               ' "800px*600px"'
    subprocess.call(image_generation_command, shell=True)

    json_resonse = {'image_url': os.path.join(settings.MEDIA_URL, file_name)}

    return HttpResponse(json.dumps(json_resonse), mimetype="application/json")
