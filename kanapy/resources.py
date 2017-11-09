import sys

from kanapy.api import APIClient


LIST = type([])
DICT = type({})


def from_dict(variable, module_source=__name__):
    return dict([(k, deserialize(v, module_source=module_source)) for k, v in variable.items()])


def deserialize(variable, module_source=__name__):
    if type(variable) not in [LIST, DICT]:
        return variable

    if type(variable) == LIST:
        return [deserialize(v, module_source=module_source) for v in variable]

    className = variable['resource_type']
    current_module = sys.modules[module_source]
    cls = None
    try:
        cls = getattr(current_module, className)
    except AttributeError:
        setattr(current_module, className, type(className, (Resource,), {}))
        cls = getattr(current_module, className)

    return cls(**from_dict(variable, module_source=module_source))


def _inflate(response, cls, obj=None):
    response.raise_for_status()
    if not obj:
        obj = cls()
    obj.__dict__ = response.json()['data']
    return obj, response.json().get('session_id')


class Resource:
    resouce_type = None

    def __init__(self, id=None, created_at=None, updated_at=None, resource_url=None, resource_type=None):
        self.id = id
        self.created_at = created_at
        self.updated_at = created_at
        self.resouce_url = resource_url

    @classmethod
    def create(cls, obj):
        raise NotImplementedError()

    @classmethod
    def delete(cls, id_):
        """A HTTP DELETE has not been implemented"""
        raise NotImplementedError()

    @classmethod
    def get(cls, id):
        c = APIClient()
        url = c.get_url(cls, id)
        r = c.http.get(url, verify=False)
        obj, session_id = _inflate(r, cls)
        c.use_session(session_id)

        return deserialize(obj)

    @classmethod
    def all(cls):
        c = APIClient()
        url = c.get_url(cls)
        return c.http.get(url)

    @classmethod
    def update(cls, obj):
        """A HTTP PUT has not been implemented"""
        raise NotImplementedError()

    def get_fields(self):
        d = vars(self)
        return { key: d[key] for key in d if not key.startswith('_')}


class User(Resource):
    _resource_base_url = "/users"


