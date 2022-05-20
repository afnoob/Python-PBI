from typing_extensions import Self
import msal
import requests
import json 
from nuevo import AadService
from access_token import PbiEmbedService

authority_url = 'https://login.microsoftonline.com/d2b212c6-a5d2-4c2b-b7ba-b63e635373ad'
# authentication details
client_id= '470d230c-7279-448f-bd73-6c35de3b0816' 
client_secret = 't687Q~G2EW-XVwjFRySt_HJLjGGV0nmKwKsDW' # needed if authenticating with acquire_token_for_client function
username = 'departamentoti@ingetec.com.co' # needed if authenticating with acquire_token_by_username_password function
password = '69D0kv1XZ' # needed if authenticating with acquire_token_by_username_password function
scope =['https://analysis.windows.net/powerbi/api/.default']
result = None
# ---------------------------------------
# Option 1 for getting the token. If you don't want any credentials saved or the user has multi-factor configured on their account, the user can interactively authenticate
# ---------------------------------------

def get_token_interactive(scope):
 app = msal.PublicClientApplication(client_id, authority=authority_url)
 result = app.acquire_token_interactive(scope)
 if 'access_token' in result:
    return(result['access_token'])
 else:
    print('Error in get_token_interactive:',result.get("error"), result.get("error_description"))

# ---------------------------------------
# Option 2 for getting the token. You can save the username and password and get a token without interacting
# ---------------------------------------

def get_token_username_password(scope):
 app = msal.PublicClientApplication(client_id, authority=authority_url)
 result = app.acquire_token_by_username_password(username=username,password=password,scopes=scope)
 if 'access_token' in result:
    return(result['access_token'])
 else:
    print('Error in get_token_username_password:',result.get("error"), result.get("error_description"))

# ---------------------------------------
# Option 3 for getting the token. If authenticating via client/client_secret
# ---------------------------------------

def get_token_for_client(scope):
 app = msal.ConfidentialClientApplication(client_id,authority=authority_url,client_credential=client_secret)
 result = app.acquire_token_for_client(scopes=scope)
 if 'access_token' in result:
    return(result['access_token'])
 else:
    print('Error in get_token_username_password:',result.get("error"), result.get("error_description"))

 url = 'https://api.powerbi.com/v1.0/myorg/groups/0a14a48a-22e2-46f8-81e5-ffbca64d84fd/reports/a8cb05bd-6b0e-4c73-87b7-03103aaed332/GenerateToken'
 body = {'accessLevel': 'View', 'datasetId': '8e8b1430-4e0b-4d85-b036-ee7404c9fba4'}
 headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + result['access_token']}
 r = requests.post(url, data=json.dumps(body), headers=headers)
 if 'token' in r.text:
    return(r.text[220:1951])
 else:
    print('Error in AccessToken generation')

def nuevo_token():
   PbiEmbedService().get_embed_params_for_single_report('0a14a48a-22e2-46f8-81e5-ffbca64d84fd', 'a8cb05bd-6b0e-4c73-87b7-03103aaed332')

nuevo_token()