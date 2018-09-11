import requests
import os
from app.parse import FANTASY_DATA_KEY 
import json
from app.models import News

def get_news():
 
    uri = 'https://api.fantasydata.net/v3/nfl/stats/json/News?key=%s' % FANTASY_DATA_KEY
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
  
    newsitems = json.loads(resp.text)
    for news in newsitems:
        news, created = News.objects.get_or_create(
            NewsID=news['NewsID'],
            Updated=news['Updated'],
            Title=news['Title'],
            Content=news['Content'],
            PlayerID=news['PlayerID'],
            TeamID=news['TeamID'],
            Team=news['Team'],
        )
        print "created: {}".format(created)
        print news
        
    """
    <News>
        <NewsID>59893</NewsID>
        <Source>RotoBaller</Source>
        <Updated>2017-09-01T08:25:10</Updated>
        <TimeAgo>2 hours ago</TimeAgo>
        <Title>Kenyan Drake Plunges Into End Zone on Thursday</Title>
        <Content>Miami Dolphins running back Kenyan Drake carried eight times for 27 yards as the lead back in Thursday's preseason game.</Content>
        <Url>https://www.rotoballer.com/player-news/kenyan-drake-plunges-into-end-zone-on-thursday/408792</Url>
        <TermsOfUse>RotoBaller news feed is provided for limited commercial and non-commercial use. Attribution and hyperlink to RotoBaller.com must be provided in connection with your use of the feeds. Upgrade to RotoBaller Premium News Feeds to unlock additional premium content with full fantasy analysis, and an unlimited commercial use license. Email sales@fantasydata.com for more information.</TermsOfUse>
        <Author>Pierre Camus</Author>
        <Categories>Waivers</Categories>
        <PlayerID>18003</PlayerID>
        <TeamID>19</TeamID>
        <Team>MIA</Team>
        <PlayerID2 i:nil="true" />
        <TeamID2 i:nil="true" />
        <Team2 i:nil="true" />
    </News>
    """ 