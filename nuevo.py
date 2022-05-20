import msal

class AadService:
    
    def get_access_token():
        AUTHENTICATION_MODE = 'ServicePrincipal'

        # Workspace Id in which the report is present
        WORKSPACE_ID = '0a14a48a-22e2-46f8-81e5-ffbca64d84fd'
    
        # Report Id for which Embed token needs to be generated
        REPORT_ID = 'a8cb05bd-6b0e-4c73-87b7-03103aaed332'
    
        # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
        TENANT_ID = 'd2b212c6-a5d2-4c2b-b7ba-b63e635373ad'
    
        # Client Id (Application Id) of the AAD app
        CLIENT_ID = '470d230c-7279-448f-bd73-6c35de3b0816'
        
        # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
        CLIENT_SECRET = 't687Q~G2EW-XVwjFRySt_HJLjGGV0nmKwKsDW'
        
        # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
        SCOPE = ['https://analysis.windows.net/powerbi/api/.default']
        
        # URL used for initiating authorization request
        AUTHORITY = 'https://login.microsoftonline.com/organizations'
        
        # Master user email address. Required only for MasterUser authentication mode.
        POWER_BI_USER = ''
        
        # Master user email password. Required only for MasterUser authentication mode.
        POWER_BI_PASS = ''
        '''Generates and returns Access token

        Returns:
            string: Access token
        '''

        response = None
        try:
            if AUTHENTICATION_MODE.lower() == 'masteruser':

                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
                accounts = clientapp.get_accounts(username=POWER_BI_USER)
                
                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(SCOPE, account=accounts[0])
                    
                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(POWER_BI_USER, POWER_BI_PASS, scopes=SCOPE)     
                    
            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif AUTHENTICATION_MODE.lower() == 'serviceprincipal':
                authority = AUTHORITY.replace('organizations', TENANT_ID)
                clientapp = msal.ConfidentialClientApplication(CLIENT_ID, client_credential=CLIENT_SECRET, authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=SCOPE)
                
            try:
                return (response['access_token'])
            except KeyError:
                return(Exception(response['error_description']))
                
        except Exception as ex:
            return(Exception('Error retrieving Access token\n' + str(ex)))



