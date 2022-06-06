#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/6 10:50
# @Author   : StephenZ
# @Site     : 
# @File     : tt.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/16 8:28
# @Author   : StephenZ
# @Site     :
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
# !/usr/bin/env python3
# coding: utf-8

import re
from lxml import etree
import requests
import time
import json
import urllib


proxy = "127.0.0.1:7890"

proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy
}

data = {
    "debug": True,
    "log": """
    [{"_category_":"client_event","format_version":2,"triggered_on":1654076830603,"items":[{"item_type":8,"item_query":"#ArtıkFazlaOldunuz","name":"#ArtıkFazlaOldunuz","guide_item_details":{"item_type":"DAABDAABCwABAAAADXRyZW5kc19tb2R1bGULAAIAAAAGdHJlbmRzAAAPAAIMAAAAAQwAAQsAAQAAAA10cmVuZHNfbW9kdWxlCwACAAAABnRyZW5kcwAAAA==","source_data":"CwABAAAAJGE4ZjRmODc4LWIwMGItNGVhNy1iNmZkLTY5NWFkZDNmYmYwYQsAAgAAADY6bG9jYXRpb25fcmVxdWVzdDpoYXNodGFnX3RyZW5kOnRheGlfd29ybGR3aWRlX3NvdXJjZToGAAMAAAsABAAAABMjQXJ0xLFrRmF6bGFPbGR1bnV6AgANAAA=","transparent_guide_details":{"trendMetadata":{"impressionId":"a8f4f878-b00b-4ea7-b6fd-695add3fbf0a","impressionToken":":location_request:hashtag_trend:taxi_worldwide_source:","position":0,"trendName":"#ArtıkFazlaOldunuz","containsCuratedTitle":false}}},"impression_details":{"visibility_start":1654076822621,"visibility_end":1654076830602}},{"item_type":8,"item_query":"LGBTQ","name":"LGBTQ","guide_item_details":{"item_type":"DAABDAABCwABAAAADXRyZW5kc19tb2R1bGULAAIAAAAGdHJlbmRzAAAPAAIMAAAAAQwAAQsAAQAAAA10cmVuZHNfbW9kdWxlCwACAAAABnRyZW5kcwAAAA==","source_data":"CwABAAAAJGE4ZjRmODc4LWIwMGItNGVhNy1iNmZkLTY5NWFkZDNmYmYwYQsAAgAAADU6bG9jYXRpb25fcmVxdWVzdDplbnRpdHlfdHJlbmQ6dGF4aV93b3JsZHdpZGVfc291cmNlOgYAAwABCwAEAAAABUxHQlRRDwAFCwAAAAEAAAAII2xnYnRxaWECAA0AAA==","transparent_guide_details":{"trendMetadata":{"impressionId":"a8f4f878-b00b-4ea7-b6fd-695add3fbf0a","impressionToken":":location_request:entity_trend:taxi_worldwide_source:","position":1,"trendName":"LGBTQ","relatedTerms":["#lgbtqia"],"containsCuratedTitle":false}}},"impression_details":{"visibility_start":1654076822621,"visibility_end":1654076830602}},{"item_type":8,"item_query":"ZAM ZAM ZAM","name":"ZAM ZAM ZAM","guide_item_details":{"item_type":"DAABDAABCwABAAAADXRyZW5kc19tb2R1bGULAAIAAAAGdHJlbmRzAAAPAAIMAAAAAQwAAQsAAQAAAA10cmVuZHNfbW9kdWxlCwACAAAABnRyZW5kcwAAAA==","source_data":"CwABAAAAJGE4ZjRmODc4LWIwMGItNGVhNy1iNmZkLTY5NWFkZDNmYmYwYQsAAgAAADU6bG9jYXRpb25fcmVxdWVzdDplbnRpdHlfdHJlbmQ6dGF4aV93b3JsZHdpZGVfc291cmNlOgYAAwACCwAEAAAAC1pBTSBaQU0gWkFNAgANAAA=","transparent_guide_details":{"trendMetadata":{"impressionId":"a8f4f878-b00b-4ea7-b6fd-695add3fbf0a","impressionToken":":location_request:entity_trend:taxi_worldwide_source:","position":2,"trendName":"ZAM ZAM ZAM","containsCuratedTitle":false}}},"impression_details":{"visibility_start":1654076822621,"visibility_end":1654076830602}}],"event_namespace":{"page":"search","section":"sidebar","component":"stream","element":"linger","action":"results","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":37,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832913,"items":[{"item_type":0,"id":"1529149865724456964","position":2,"sort_index":"999970","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAAAEAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"percent_screen_height_100k":77782,"author_id":"1481260053499895810","quoted_tweet_id":"1528788298562428930","quoted_author_id":"1419588531584966656","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"engagement_metrics":{"reply_count":0,"retweet_count":81,"favorite_count":118,"quote_count":0}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"stream","action":"results","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":38,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832932,"search_details":{"query":"抖音","social_filter":"all","near":"anywhere"},"items":[{"item_type":0,"id":"1529082699255795719","position":1,"sort_index":"999980","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAAIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"author_id":"1202343077328965634","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":0,"retweet_count":4,"favorite_count":7,"quote_count":0},"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","video_uuid":"1529082646449602560","video_owner_id":"1202343077328965634","video_type":"video","content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","client_media_event":{"media_client_event_type":{"intent_to_play":{}},"session_state":{"session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","content_video_identifier":{"media_platform_identifier":{"media_category":7,"media_id":"1529082646449602560"}},"tweet_id":"1529082699255795719"},"playing_media_state":{"video_type":2,"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","media_metadata":{"twitter_publisher_id":"1202343077328965634","publisher_identifier":{"twitter_publisher_identifier":{"id":"1202343077328965634"}}}},"player_state":{"is_muted":false}},"live_broadcast_details":{},"live_video_event_details":{}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"result","element":"video_player","action":"intent_to_play","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":39,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832957,"search_details":{"query":"抖音","social_filter":"all","near":"anywhere"},"items":[{"item_type":0,"id":"1529082699255795719","position":1,"sort_index":"999980","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAAIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"author_id":"1202343077328965634","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":0,"retweet_count":4,"favorite_count":7,"quote_count":0},"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","video_uuid":"1529082646449602560","video_owner_id":"1202343077328965634","video_type":"video","content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","client_media_event":{"media_client_event_type":{"mute":{}},"session_state":{"session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","content_video_identifier":{"media_platform_identifier":{"media_category":7,"media_id":"1529082646449602560"}},"tweet_id":"1529082699255795719"},"playing_media_state":{"video_type":2,"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","media_metadata":{"twitter_publisher_id":"1202343077328965634","publisher_identifier":{"twitter_publisher_identifier":{"id":"1202343077328965634"}}}},"player_state":{"is_muted":false}},"live_broadcast_details":{},"live_video_event_details":{}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"result","element":"video_player","action":"mute","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":40,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832973,"search_details":{"query":"抖音","social_filter":"all","near":"anywhere"},"items":[{"item_type":0,"id":"1531322508196061187","position":0,"sort_index":"999990","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAgIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"author_id":"1525940373553651712","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1531322437039702016","publisher_id":"1525940373553651712","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":8,"retweet_count":27,"favorite_count":96,"quote_count":0},"media_asset_url":"https://video.twimg.com/ext_tw_video/1531322437039702016/pu/pl/hAZqhfmNwTTopW92.m3u8?tag=12&container=fmp4","video_uuid":"1531322437039702016","video_owner_id":"1525940373553651712","video_type":"video","content_id":"1531322437039702016","publisher_id":"1525940373553651712","media_session_id":"6a8815d2-2060-4717-8333-124b86365b45","client_media_event":{"media_client_event_type":{"pause":{}},"session_state":{"session_id":"6a8815d2-2060-4717-8333-124b86365b45","content_video_identifier":{"media_platform_identifier":{"media_category":7,"media_id":"1531322437039702016"}},"tweet_id":"1531322508196061187"},"playing_media_state":{"video_type":2,"media_asset_url":"https://video.twimg.com/ext_tw_video/1531322437039702016/pu/pl/hAZqhfmNwTTopW92.m3u8?tag=12&container=fmp4","media_metadata":{"twitter_publisher_id":"1525940373553651712","publisher_identifier":{"twitter_publisher_identifier":{"id":"1525940373553651712"}}}},"player_state":{"is_muted":true}},"live_broadcast_details":{},"live_video_event_details":{}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"result","element":"video_player","action":"pause","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":41,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832974,"search_details":{"query":"抖音","social_filter":"all","near":"anywhere"},"items":[{"item_type":0,"id":"1531322508196061187","position":0,"sort_index":"999990","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAgIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"author_id":"1525940373553651712","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1531322437039702016","publisher_id":"1525940373553651712","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":8,"retweet_count":27,"favorite_count":96,"quote_count":0},"media_asset_url":"https://video.twimg.com/ext_tw_video/1531322437039702016/pu/pl/hAZqhfmNwTTopW92.m3u8?tag=12&container=fmp4","video_uuid":"1531322437039702016","video_owner_id":"1525940373553651712","video_type":"video","content_id":"1531322437039702016","publisher_id":"1525940373553651712","media_session_id":"6a8815d2-2060-4717-8333-124b86365b45","client_media_event":{"media_client_event_type":{"heartbeat":{"buffering_duration_millis":"0","buffering_count":0,"percent_in_view":64,"sampled_bits_per_second":922409,"data_usage_bytes":"0","start_program_date_time_millis":"0","end_program_date_time_millis":"2786","audible_duration_millis":"0","bitrate_metrics":{"min_bps":922409,"max_bps":922409,"avg_bps":922409},"live_or_non_live_heartbeat_metrics":{"non_live_heartbeat_metrics":{}}}},"session_state":{"session_id":"6a8815d2-2060-4717-8333-124b86365b45","content_video_identifier":{"media_platform_identifier":{"media_category":7,"media_id":"1531322437039702016"}},"tweet_id":"1531322508196061187"},"playing_media_state":{"video_type":2,"media_asset_url":"https://video.twimg.com/ext_tw_video/1531322437039702016/pu/pl/hAZqhfmNwTTopW92.m3u8?tag=12&container=fmp4","media_metadata":{"twitter_publisher_id":"1525940373553651712","publisher_identifier":{"twitter_publisher_identifier":{"id":"1525940373553651712"}}}},"player_state":{"is_muted":true}},"buffering_duration_millis":0,"video_visibility":64,"start_program_date_time_millis":0,"end_program_date_time_millis":2786,"sampled_bitrate":922409,"data_usage_bytes":0,"live_broadcast_details":{},"live_video_event_details":{}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"result","element":"video_player","action":"heartbeat","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":42,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832981,"search_details":{"query":"抖音","social_filter":"all","near":"anywhere"},"items":[{"item_type":0,"id":"1529082699255795719","position":1,"sort_index":"999980","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAAIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"author_id":"1202343077328965634","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":0,"retweet_count":4,"favorite_count":7,"quote_count":0},"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","video_uuid":"1529082646449602560","video_owner_id":"1202343077328965634","video_type":"video","content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","client_media_event":{"media_client_event_type":{"play":{}},"session_state":{"session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","content_video_identifier":{"media_platform_identifier":{"media_category":7,"media_id":"1529082646449602560"}},"tweet_id":"1529082699255795719"},"playing_media_state":{"video_type":2,"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","media_metadata":{"twitter_publisher_id":"1202343077328965634","publisher_identifier":{"twitter_publisher_identifier":{"id":"1202343077328965634"}}}},"player_state":{"is_muted":true}},"live_broadcast_details":{},"live_video_event_details":{}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"result","element":"video_player","action":"play","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":43,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076832986,"search_details":{"query":"抖音","social_filter":"all","near":"anywhere"},"items":[{"item_type":0,"id":"1529082699255795719","position":1,"sort_index":"999980","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAAIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"author_id":"1202343077328965634","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":0,"retweet_count":4,"favorite_count":7,"quote_count":0},"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","video_uuid":"1529082646449602560","video_owner_id":"1202343077328965634","video_type":"video","content_id":"1529082646449602560","publisher_id":"1202343077328965634","media_session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","client_media_event":{"media_client_event_type":{"playback_start":{"latency_millis":58,"cache_info":{"notCached":{}}}},"session_state":{"session_id":"0d9e4773-cffc-40d1-885b-c3ba4982e402","content_video_identifier":{"media_platform_identifier":{"media_category":7,"media_id":"1529082646449602560"}},"tweet_id":"1529082699255795719"},"playing_media_state":{"video_type":2,"media_asset_url":"https://video.twimg.com/ext_tw_video/1529082646449602560/pu/pl/mv_JWveoT3vd1bhf.m3u8?tag=12&container=fmp4","media_metadata":{"twitter_publisher_id":"1202343077328965634","publisher_identifier":{"twitter_publisher_identifier":{"id":"1202343077328965634"}}}},"player_state":{"is_muted":true}},"latency":58,"live_broadcast_details":{},"live_video_event_details":{}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"result","element":"video_player","action":"playback_start","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":44,"client_app_id":"3033300"},{"_category_":"client_event","format_version":2,"triggered_on":1654076833196,"items":[{"item_type":0,"id":"1531322508196061187","position":0,"sort_index":"999990","suggestion_details":{"controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAAAgIAAAAwAAgoAAQAAAAAAAAABCgACtqjyufquK8ELAAMAAAAG5oqW6Z+zCgAFO6qv2BVACuEAAAAAAA=="},"impression_details":{"visibility_start":1654076823336,"visibility_end":1654076832842},"author_id":"1525940373553651712","is_viewer_follows_tweet_author":false,"is_tweet_author_follows_viewer":false,"is_viewer_super_following_tweet_author":false,"is_viewer_super_followed_by_tweet_author":false,"is_tweet_author_super_followable":false,"media_details":{"photo_count":0,"content_id":"1531322437039702016","publisher_id":"1525940373553651712","media_type":1,"dynamic_ads":false},"engagement_metrics":{"reply_count":8,"retweet_count":27,"favorite_count":96,"quote_count":0}}],"event_namespace":{"page":"search","section":"search_filter_top","component":"stream","element":"linger","action":"results","client":"m5"},"client_event_sequence_start_timestamp":1654076820920,"client_event_sequence_number":45,"client_app_id":"3033300"}]
    """
}


# with requests.get("https://t.co/zjx956C8ED", proxies=proxies) as session:
#     print(session.text)


import arrow
import stweet as st
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ProxyConfig = st.RequestsWebClientProxyConfig(
    http_proxy="127.0.0.1:7890",
    https_proxy="127.0.0.1:7890"
)

since = arrow.get('2022-06-01')
until = arrow.get('2022-06-02')

search_tweets_task = st.SearchTweetsTask(
    exact_words="抖音风",
    since=since,
    until=until,
    replies_filter=st.RepliesFilter.ONLY_ORIGINAL,
)

st.TweetSearchRunner(
    search_tweets_task=search_tweets_task,
    tweet_outputs=[st.CsvTweetOutput('nijisanji_20211001_20211002.csv'), st.PrintTweetOutput()],
    web_client=st.RequestsWebClient(proxy=ProxyConfig, verify=False),
).run()








import re, requests
from pathlib import Path
from bs4 import BeautifulSoup
from shutil import copyfileobj
from urllib.parse import quote as qt

HEADERS = {
    'authority': 'twittervideodownloader.com',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


class TwitterMediaContent:
    url = None
    type = None
    filename = None

    def __init__(self, url, type, filename):
        self.url = url
        self.type = type
        self.filename = filename

    def __getitem__(self, name):
        if name == 'url':
            return self.url

        if name == 'type':
            return self.type

        if name == 'filename':
            return self.filename


class TwitterMedia:
    def __init__(self, use_print=False):
        self._token = ''
        self._is_token_generated = False
        self._use_print = use_print
        self.main_page = 'https://twittervideodownloader.com/'
        self.download_page = 'https://twittervideodownloader.com/download'

    def browser(self, post, url, **kwargs):
        with requests.Session() as session:
            if post:
                return session.post(url, headers=kwargs['headers'], proxies=proxies, cookies=kwargs['cookies'], data=kwargs['rawdata'])
            else:
                return session.get(url, proxies=proxies, stream=True)

    def download(self, url, custom=None):
        filename = (url.split('/')[-1]).split('?')[0]
        if custom:
            filename = f'{custom}.mp4'

        with self.browser(0, url) as data:
            with open(filename, 'wb') as video:
                copyfileobj(data.raw, video)

        return filename

    def fetch_media(self, url):
        self._generate_token()

        html = self.browser(
            1,
            self.download_page,
            cookies={'csrftoken': self._token},
            rawdata=f'csrfmiddlewaretoken={self._token}&tweet={qt(url)}&submit=',
            headers={
                **HEADERS,
                'referer': self.main_page
            }
        )

        content = html.content

        if 'Download Video' not in str(content):
            self._print('Deleting the csrf token!')
            if Path('csrftoken').is_file():
                Path('csrftoken').unlink()
            return

        urls, res = [], []

        statusID = re.findall(r'status/([\d.]*\d+)', url)
        username = re.findall('.com/(.*)/status', url)
        filename = '{}_{}'.format(username[0], statusID[0])
        soup = BeautifulSoup(content, 'html.parser')

        for url in soup.select('a.expanded.button.small.float-right'):
            urls.append(url['href'])

        if len(urls) == 1:
            return TwitterMediaContent(urls[0], 'gif', filename)
        else:
            for url in urls:
                resolution = re.search(r'/[0-9]*x[0-9]*/', url).group(0)
                res.append(int((resolution.replace('/', '')).split('x')[1]))
            return TwitterMediaContent(urls[res.index(max(res))], 'video', filename)

    def _generate_token(self):
        # FIXME: Should we instead look for self.token only?
        if self._is_token_generated:
            return

        if Path('csrftoken').exists():
            with open('csrftoken', 'r') as f:
                self._token = f.readline()

            self._print('Loaded the csrf token from cache.\n')
        else:
            session = self.browser(0, self.main_page)
            self._print(session.cookies)
            csrftoken = session.cookies['csrftoken']

            self._token = csrftoken
            with open('csrftoken', 'w') as f:
                f.write(csrftoken)

            self._print('Created a new csrf token!\n')

        self._is_token_generated = True

    def _print(self, *args):
        if self._use_print:
            print(*args)

# Create an instance
downloader = TwitterMedia()

# Fetch media through an URL
tweet = downloader.fetch_media('https://twitter.com/i/status/1531974111831916545')

# Will print the url
print(tweet.url)

# Will print the type, it could either be 'video' or 'gif'
# Twitter keeps gif files in mp4 format
# So if you want to convert them to actual gifs,
# you can use this key to check if the media is a gif or not
# print(tweet.type)

# You can download through the download function with the url key
# It will return a filename upon downloading
# dl_filename = downloader.download(tweet.url)

# You can also assign custom filenames to the downloaded file
# The extension is always '.mp4' for twitter media, be it video or a gif
# downloader.download(tweet.url, custom = 'custom_name')

# Download with username and status id
# downloader.download(tweet.url, custom = tweet.filename)