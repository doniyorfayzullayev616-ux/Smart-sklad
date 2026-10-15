from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code

        # if isinstance(data, dict) and 'results' in data:
        #     data = data['results']

        response_data = {
            "success": 200 <= status_code < 300,
            "data": data if 200 <= status_code <300 else None,
            "error": data if status_code >= 400 else None
        }

        return super().render(response_data, accepted_media_type, renderer_context)