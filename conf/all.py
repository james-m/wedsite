#######
# CONFIG SETUP do not change or configs will break
#    this goes a the top of any config file. it adds stuff to the global config
#    context. 
import context
cfg = context.ctx()
cfg.push(__name__)
# END CONFIG SETUP
#######
cfg.appname = 'jamesandnancywed.com'



################
# REMOTE LOGGING GLOBALS 
#

################
# FACEBOOK GLOBALS 
#

cfg.FBAPI_SCOPE = [
    'email',
    'user_about_me',
    'user_birthday',
    'user_education_history',
    'user_hometown',
    'user_groups',
    'user_interests',
    'user_questions',
    'user_relationships',
    'user_work_history',
    'friends_education_history',
    'friends_work_history',
    ]
cfg.FBAPI_CREDS = {
	#http://developers.facebook.com/docs/reference/api/permissions/
	'FBAPI_APP_ID': 'replace',
	'FBAPI_APP_NAME': 'replace',
	'FBAPI_APP_SECRET': 'replace',
	'FBAPI_REDIRECT_URI': 'replace'
}

cfg.FBAPI_URIS = {	
	#http://developers.facebook.com/docs/authentication/
	'GRAPH_BASE_URI' : 'https://graph.facebook.com/',
	'OAUTH_DIA_URI' : 'https://www.facebook.com/dialog/oauth',
	'APP_AUTH_URI' : 'https://graph.facebook.com/oauth/access_token',
}

################
# GENERIC SERVICE GLOBALS
#
cfg.SERVICE_SHUTDOWN_TIMEOUT = 120
cfg.SERVICE_SHUTDOWN_DEADMAN = 300
cfg.SERVICE_DB_POOL_TIMEOUT  = 15

################
# WEB SERVICE GLOBALS
#
cfg.WEB_SRV_DEBUG = False 
cfg.WEB_SRV_AUTORELOAD = False 




