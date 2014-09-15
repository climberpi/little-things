#encoding=utf-8
import webbrowser
import json
from weibo import APIClient

# necessary information
APP_KEY = ''
APP_SECRET = ''
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
client = APIClient(APP_KEY,APP_SECRET,CALLBACK_URL)  
authorize_url = client.get_authorize_url(redirect_uri = CALLBACK_URL)

# open browser, and get auth_code manually
webbrowser.open(authorize_url)
code = raw_input("input the code: ").strip()

# get user's auth
request = client.request_access_token(code) # request access_token
access_token = request.access_token 
expires_in = request.expires_in  

# linked server success
print 'Successfully get access_token:',access_token
print 'Successfully get expires_in:',expires_in
client.set_access_token(access_token, expires_in)

# weibo analysis
state = open('state.csv', 'w')#, encoding = 'utf-8') 
# write the head of from
line = "id\tnickname\tcreated_at\treposts_count\tcomments_count\ttext\ttype\n" 
state.write(line)
state.flush()
# in this case, 100x10 pieces of weibo will be recorded, i.e. total equal to count multiply page.
TotalPage = 10
# a const array to mark every weibo's type.
TypeArray = {1:"normal", 2:"picture", 3:"video", 4:"music"}
for PAGE in range(1, TotalPage+1):
    # get weibo list from API
    for FEATURE in range(1, 5):
        # mark every weibo's type
        TYPE = TypeArray[FEATURE]
        # try to get weibos satisfied certain PAGE and certain FEATURE(type)
        text = client.statuses.home_timeline.get(count=100, page=PAGE, feature=FEATURE)
        for item in text["statuses"]:
            # weibo's author's uid
            line = str(item["id"]) + '\t'
            # weibo's author's nickname(screen name)
            line += item["user"]["screen_name"].encode("utf-8") + '\t'
            # weibo's created time
            line += item["created_at"].encode("utf-8") + '\t'
            line += str(item["reposts_count"]) + '\t'
            line += str(item["comments_count"]) + '\t'
            line += item["text"].encode("utf-8") + '\t'
            # weibo's type/feature
            line += TYPE + '\n'
            # write this line into file
            state.write(line)
            state.flush()
state.close()
