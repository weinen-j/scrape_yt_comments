# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import csv
import googleapiclient.discovery
import pandas as pd


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBl1LoyjrbxOhv7fmUR2Is_PkbQk-_EbbM"
    video_id = {"2xlol-SNQRU"}

    commentthread = []

    for i in video_id:

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=10,
            order="relevance",
            textFormat="plainText",
            videoId=i
        )
        response = request.execute()
        print(response)
        comments = []
        reply = []
        comments.append("id" + "§" + "text" + "§" + "videoID")

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_id = item['snippet']['videoId']
            top_comment_id = item['id']

            request_replies = youtube.comments().list(
                part="snippet",
                maxResults=1,
                parentId=top_comment_id
            )
            replies = request_replies.execute()

            for x in replies['items']:
                reply_snip = x['snippet']['textOriginal']
                reply.append(reply_snip)

            comments.append(comment + '§' + comment_id)
            comments.append(reply_snip + '§' + comment_id)

        commentthread.append(comments)

    # print(top_comment_id)

    flattened = []
    for sublist in commentthread:
        for val in sublist:
            flattened.append(val)

    # print(flattened)
    out = pd.DataFrame.from_dict(flattened)
    pd.DataFrame()

    out.to_csv('output.csv', sep='§', encoding='utf-8')


if __name__ == "__main__":
    main()  # -*- coding: utf-8 -*-
