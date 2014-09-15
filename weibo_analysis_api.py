#encoding=utf-8
import webbrowser
import json
from weibo import APIClient

# necessary information
# [configure reference] http://blog.csdn.net/minenki/article/details/8836293
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
# in this case, 100x10 pieces of weibo will be recorded, i.e. total equal to count multiply page.
TotalPage = 10
# a const array to mark every weibo's type.
TypeArray = {1:"normal", 2:"picture", 3:"video", 4:"music"}
WeiboList = {}
for PAGE in range(1, TotalPage+1):
    # get weibo list from API
    for FEATURE in range(1, 5):
        # mark every weibo's type
        TYPE = TypeArray[FEATURE]
        # try to get weibos satisfied certain PAGE and certain FEATURE(type)
        text = client.statuses.home_timeline.get(count=100, page=PAGE, feature=FEATURE)
        for item in text["statuses"]:
            Weibo = {}
            def initialize():
                # weibo's author's uid
                Weibo["id"] = str(item["id"])
                # weibo's author's nickname(screen name)
                Weibo["nickname"] = item["user"]["screen_name"].encode("utf-8") 
                # weibo's created time
                Weibo["created_at"] = item["created_at"].encode("utf-8")
                Weibo["reposts_count"] = str(item["reposts_count"]) 
                Weibo["comments_count"] = str(item["comments_count"]) 
                Weibo["text"] = item["text"].encode("utf-8") 
                # intialize weibo's type
                Weibo["normal"] = Weibo["picture"] = Weibo["video"] = Weibo["music"] = False
            # use id+created_at as key
            Key = str(item["id"])+item["created_at"].encode("utf-8")
            if Key in WeiboList:
                Weibo = WeiboList[Key]
            else: 
                initialize()
            # weibo's type/feature
            Weibo["normal"] |= (FEATURE == 1)
            Weibo["picture"] |= (FEATURE == 2)
            Weibo["video"] |= (FEATURE == 3)
            Weibo["music"] |= (FEATURE == 4)
            # update weibo's analysis
            WeiboList[Key] = Weibo

# write weibos' analysis to file
state = open('state.csv', 'w') 
SeparateMark = "\t"
# write the head of from
line = "id" + SeparateMark + "nickname" + SeparateMark + "created_at" + SeparateMark + "reposts_count"+ SeparateMark +"comments_count" + SeparateMark + "text" + SeparateMark + "normal" + SeparateMark + "picture" + SeparateMark + "video" + SeparateMark + "music\n" 
state.write(line)
state.flush()
for WeiboKey in WeiboList.items():
    # generate every weibo's analysis
    Weibo = WeiboKey[1]
    line = Weibo["id"] + SeparateMark 
    line += Weibo["nickname"] + SeparateMark 
    line += Weibo["created_at"] + SeparateMark
    line += Weibo["reposts_count"] + SeparateMark
    line += Weibo["comments_count"] + SeparateMark
    line += Weibo["text"] + SeparateMark
    line += str(Weibo["normal"]) + SeparateMark
    line += str(Weibo["picture"]) + SeparateMark
    line += str(Weibo["video"]) + SeparateMark
    line += str(Weibo["music"]) + '\n'
    # write to file
    state.write(line)
    state.flush()
state.close()
