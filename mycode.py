with open("key.txt",'r') as f:
  api_key=f.read()
from googleapiclient.discovery import build
resource = build("youtube", "v3", developerKey=api_key)
req1=resource.search().list(part="snippet",type="video",q="avatar movie",maxResults=1)
res1=req1.execute()
details1=res1["items"][0]
id1=details1["id"]
print(id1)
snippet_details1=details1["snippet"]
print(snippet_details1)
channel_id1=snippet_details1["channelId"]
v_desc1=snippet_details1["description"]
c_title1=snippet_details1["channelTitle"]
v_title1=snippet_details1["title"]
print("The channel id is ->"+channel_id1+" ,has video description ->"+v_desc1+" ,has channel title ->"+c_title1+" , and has video title as ->"+v_title1)
import pandas as pd
req2=resource.search().list(part="snippet",type="video",q="avatar movie",maxResults=50,regionCode="US",order="relevance")
res2=req2.execute()
columns=["video ID","Title","no of views","no of likes","no of comments"]
df=pd.DataFrame(columns=columns)
for i in range(50):
  try:
    smaller_part=res2["items"][i]
    vid=smaller_part["id"]["videoId"]
    title=smaller_part["snippet"]["title"]
    req_for_stats= resource.videos().list(part="snippet,statistics",id=vid)
    res_for_stats= req_for_stats.execute()
    res_for_stats=res_for_stats["items"][0]
    stats=res_for_stats["statistics"]
    no_of_views=stats["viewCount"]
    no_of_likes=stats["likeCount"]
    no_of_comments=stats["commentCount"]
    lis=[vid,title,no_of_views,no_of_likes,no_of_comments]
    df.loc[len(df)] = lis
  except:
    continue
df.to_csv("answer.csv", index=False)
df["no of comments"] = pd.to_numeric(df["no of comments"])
sorted_df=df.sort_values(by="no of comments",ascending=False)
final_df=sorted_df[["video ID","Title",]].head(n=10)
from pprint import pprint
jsonlis=[]
for x in final_df["video ID"]:
  comment_request = resource.commentThreads().list(part="snippet",videoId=x)
  comment_response = comment_request.execute()
  jsonlis.append(comment_response)
for item in jsonlis:
  pprint(item)
import json
filename="Answerforpart3b.json"
for i in range(10):
  with open(filename, 'a') as json_file:
      json.dump(jsonlis[i], json_file)
for k in range(10):
  vidlikesvsviews=final_df.iloc[k,0]
  req_like_vs_views= resource.videos().list(part="snippet,statistics",id=vidlikesvsviews)
  res_like_vs_views= req_like_vs_views.execute()
  s=res_like_vs_views["items"][0]["statistics"]
  l=int(s["likeCount"])
  v=int(s["viewCount"])
  print(final_df.iloc[k,1]+ " ->" +str(l/v))
