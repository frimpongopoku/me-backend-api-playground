from _main_.settings import IS_PROD, IS_LOCAL

ME_SUPPORT_TEAM_EMAIL = "support@me.org"
# API user types

STANDARD_USER = 'standard_user'
GUEST_USER = 'guest_user'
INVITED_USER = 'invited_user'    

if (IS_PROD):
  DATA_DOWNLOAD_TEMPLATE_ID = "28578196"
  EMAIL_POSTMARK_TEMPLATE_GUEST_USER_EMAIL = "28578197"
  SADMIN_EMAIL_TEMPLATE_ID = "28578198"
  CADMIN_EMAIL_TEMPLATE_ID = "28578195"
  EMAIL_POSTMARK_TEMPLATE_USER_WELCOME = "28578199"
  GUEST_USER_EMAIL_TEMPLATE_ID = "28578197"
  WEEKLY_EVENTS_NUDGE_TEMPLATE_ID="30038176"
  YEARLY_MOU_TEMPLATE_ID = "31025296" # Change to PROD template when template is finalised before deployment
  MOU_SIGNED_ADMIN_RECEIPIENT = "31128813"
  MOU_SIGNED_SUPPORT_TEAM_TEMPLATE = "31138501"
  USER_EVENTS_NUDGE_TEMPLATE_ID = "30986598"
elif (IS_LOCAL):
 DATA_DOWNLOAD_TEMPLATE_ID = "28790436"
 EMAIL_POSTMARK_TEMPLATE_GUEST_USER_EMAIL = "28437705"
 SADMIN_EMAIL_TEMPLATE_ID = "28790439"
 CADMIN_EMAIL_TEMPLATE_ID = "28790435"
 EMAIL_POSTMARK_TEMPLATE_USER_WELCOME = "28790440"
 GUEST_USER_EMAIL_TEMPLATE_ID = "28790437"
 WEEKLY_EVENTS_NUDGE_TEMPLATE_ID="30038358"  
 YEARLY_MOU_TEMPLATE_ID = "31025307"
 MOU_SIGNED_ADMIN_RECEIPIENT = "31128813"
 MOU_SIGNED_SUPPORT_TEAM_TEMPLATE = "31138501"
 USER_EVENTS_NUDGE_TEMPLATE_ID="30986598"
else:
  DATA_DOWNLOAD_TEMPLATE_ID = "27864141"
  EMAIL_POSTMARK_TEMPLATE_GUEST_USER_EMAIL = "28437705"
  SADMIN_EMAIL_TEMPLATE_ID = "27843576"
  CADMIN_EMAIL_TEMPLATE_ID = "27853283"
  EMAIL_POSTMARK_TEMPLATE_USER_WELCOME = "27142713"
  GUEST_USER_EMAIL_TEMPLATE_ID = "28437705"
  WEEKLY_EVENTS_NUDGE_TEMPLATE_ID="29520140"
  YEARLY_MOU_TEMPLATE_ID = "31025307"
  MOU_SIGNED_ADMIN_RECEIPIENT = "31128813"
  MOU_SIGNED_SUPPORT_TEAM_TEMPLATE = "31138501"
  USER_EVENTS_NUDGE_TEMPLATE_ID="30986598"
