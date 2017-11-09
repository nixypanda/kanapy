import requests

class Borg:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

class APIClient(Borg):
    """
    A client to interact with the Kayako API

    Encapsulates the `requests` http client and maintains relevant state
    :param domain: The full domain of your desk for example
    "iluvkayako.kayako.com" or a custom domain such as "iluvkayako.com"
    :param username: Your Kayako username
    :param password: Your Kayako password
    :param session: (optional) A `requests` library Session object if you want
    to use your own


    TODO: JWT support

    """
    _api_base_url = "https://{}/api/v1"

    def __init__(self, domain=None, username=None, password=None, session=None):
        super().__init__()
        if domain:
            self._domain = domain
        if username:
            self._username = username
        if password:
            self._password = password

        if session: #if provided use it
            self._session = session
        else:
            if not hasattr(self, '_session'): #if not been set in the past create a new one
                self._session = requests.Session()
            else: #there must already be an existing session, do nothing
                pass
        self._session.auth = (self._username, self._password)


    @property
    def http(self):
        return self._session

    def get_url(self, cls, id_=None):
        url = self._api_base_url.format(self._domain) + cls._resource_base_url
        if id_:
            return url + "/" + str(id_)
        return url


    def use_session(self, session_id):
        if session_id:
            self._session.headers.update({'X-Session-ID':session_id})


# c = APIClient(<details>)
# User.all(), User.get(1)