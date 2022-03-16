from googleapiclient.discovery import build
from getpass import getpass

def youtube_videodata(video_Id):
    developer_Key = getpass()
    youtube = build('youtube','v3',developerKey=developer_Key)
    video_response=youtube.commentThreads().list(part='snippet,replies',videoId=video_Id).execute()
    result = {}
    index=0
    for item in video_response['items']:
        index+=1
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
        replycount = item['snippet']['totalReplyCount']
        if replycount > 0:
            replies =[]
            for reply in item['replies']['comments']:
                reply = reply['snippet']['textDisplay']
                replies.append(reply)
        result[index] = {'comment':comment,
                     'like count': like_count,
                     'reply count': replycount,
                     'replies': replies}
    return result
