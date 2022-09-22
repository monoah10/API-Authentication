from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        Response=''
        if 'ErrorDetail' in str(data):
            Response=json.dumps({'errors':data})
        else:
            Response=json.dumps(data)

        return Response