# Mendeley application credentials
CLIENT_ID = '637'
CLIENT_SECRET = 'iAc546o0eCnSrpna'
OAUTH_AUTHORIZE_URL = 'https://api.mendeley.com/oauth/authorize'
OAUTH_ACCESS_TOKEN_URL = 'https://api.mendeley.com/oauth/token'
API_URL = 'https://api.mendeley.com/oapi/'

# Mendeley access scope
SCOPE = ['all']

# Set Mendeley privacy on OSF permissions change
SET_PRIVACY = False

CSL_PATH = '~/Documents/mendeley-oapi-example/citeproc/data/styles'

CITATION_STYLES = {'American Political Science Association': 'american-political-science-association',
                    'American Psychological Association': 'apa',
                    'American Sociological Association' : 'american-sociological-association',
                    'Harvard Reference Format': 'harvard1',
                    'IEEE': 'ieee',
                    'Nature': 'nature'}

EXPORT_FORMATS = ['bibtex']