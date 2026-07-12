import re
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(name):
    if name.startswith('_'):
        return name
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake_dict(data):
    if isinstance(data, list):
        return [camel_to_snake_dict(item) for item in data]
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_key = camel_to_snake(k)
            new_dict[new_key] = camel_to_snake_dict(v)
        return new_dict
    return data

def snake_to_camel_dict(data):
    if isinstance(data, list):
        return [snake_to_camel_dict(item) for item in data]
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_key = snake_to_camel(k)
            new_dict[new_key] = snake_to_camel_dict(v)
        return new_dict
    return data

class CamelCaseJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        return camel_to_snake_dict(data)

class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        camel_data = snake_to_camel_dict(data)
        return super().render(camel_data, accepted_media_type, renderer_context)
