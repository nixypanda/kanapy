import sys
import inspect

from kanapy.api import APIClient
import logging


LIST = type([])
DICT = type({})
PRIMITIVE = (int, str, bool, type(None), LIST, DICT)


def to_upper_camel(snake):
    lst = snake.split("_")
    return "".join(map(lambda x: x[0].upper() + x[1:], lst))


def from_dict(variable, module_source=__name__):
    return dict([(k, deserialize(v, module_source=module_source)) for k, v in variable.items()])


def deserialize(variable, module_source=__name__):
    if type(variable) not in [LIST, DICT]:
        return variable

    if type(variable) == LIST:
        return [deserialize(v, module_source=module_source) for v in variable]

    className = to_upper_camel(variable['resource_type'])
    current_module = sys.modules[module_source]
    cls = None
    try:
        cls = getattr(current_module, className)
    except AttributeError:
        setattr(current_module, className, type(className, (Resource,), {}))
        cls = getattr(current_module, className)

    return cls(**from_dict(variable, module_source=module_source))


class Resource:
    resource_type = None

    def __init__(self, id=None, created_at=None, updated_at=None, resource_url=None, resource_type=None, **kwargs):
        self.id = id
        self.created_at = created_at
        self.updated_at = created_at
        self.resource_url = resource_url
        self.resource_type = resource_type

    @classmethod
    def create(cls, obj):
        raise NotImplementedError()

    @classmethod
    def delete(cls, id_):
        """A HTTP DELETE has not been implemented"""
        raise NotImplementedError()

    @classmethod
    def get(cls, id=None, params=None):
        c = APIClient()
        url = c.get_url(cls, id)
        response = c.http.get(url, params=params, verify=False)
        data = response.json()
        c.use_session(data.get('session_id'))

        return deserialize(data["data"])

    @classmethod
    def update(cls, obj):
        """A HTTP PUT has not been implemented"""
        raise NotImplementedError()

    def get_fields(self):
        d = vars(self)
        return { key: d[key] for key in d if not key.startswith('_')}

    def _serialize(self, val):
        if type(val) not in PRIMITIVE and issubclass(val.__class__, Resource):
            return val.serializeable()
        if type(val) is DICT:
            return {k: self._serialize(v) for k, v in val}
        if type(val) is LIST:
            return [self._serialize(v) for v in val]
        return val

    def serializable(self):
        return {k: self._serialize(v) for k, v in self.__dict__.items()}


class User(Resource):
    _resource_base_url = "/users"

    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class UserMinimal(Resource):
    _resource_base_url = "/users"

    def __init__(self, full_name=None, last_active_at=None, last_seen_at=None, avatar=None, presence_channel=None, **kwargs):
        super().__init__(**kwargs)
        self.full_name = full_name
        self.last_active_at = last_active_at
        self.last_seen_at = last_seen_at
        self.avatar = avatar
        self.presence_channel = presence_channel

    @classmethod
    def from_user(cls, user):
        return UserMinimal(
            id=user.id,
            full_name=user.full_name,
            last_active_at=user.last_active_at,
            last_seen_at=user.last_seen_at,
            avatar=user.avatar,
            presence_channel=user.presence_channel,
        )

    @classmethod
    def get(cls, id=None, params=None):
        if not id:
            users = super().get(params=params)
            return [cls.from_user(usr) for usr in users]

        user = super().get(id, params=params)
        return cls.from_user(user)


class LocaleField(Resource):
    _resource_base_url = "/locale/fields"

    def __init__(self, locale=None, translation=None, parent_id=None, field=None, **kwargs):
        super().__init__(**kwargs)
        self.locale = locale
        self.translation = translation
        self.parent_id = parent_id
        self.field = field


class Brand(Resource):
    _resource_base_url = "/brands"


class Locale(Resource):
    _resource_base_url = "/locales"
