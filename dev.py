from kanapy.api import *
c = APIClient('kashifapi.kayako.com', 'kashif@kayako.com', 'kashif@123')
try:
    u = User.get(1)
except Exception as e:
    print(e)
    print(e.response.json())
