from urllib.parse import urlparse
import environ
import base64

env = environ.Env()
environ.Env.read_env()

def getAuthHeaderForNode(id):
    # this function extracts the node origin from the url
    # it then returns the auth_header required for that node 

    # dictionary to hold username:password for remote nodes
    nodeAuthDict = {
        'tik-tak-toe-cmput404.herokuapp.com': ('admin','tX7^iS8a5Ky$^S'),
        'cmput-404-w22-group-10-backend.herokuapp.com': ('Team4','abcd1234'),
        'backend-404-2.herokuapp.com': ('copy','wxyz1234')
    }

    # extract node from url
    url_obj = urlparse(id)
    return nodeAuthDict.get(url_obj.hostname, ('',''))
    # auth_header = {}
    # encodedAuth = base64.b64encode(nodeAuthDict[url_obj.hostname].encode('ascii'))

    # auth_header = {"headers": {
    #     "Authorization": "Basic " + str(encodedAuth.decode('ascii')),
    #     "accept": 'application/json',
    # }}

    # return auth_header