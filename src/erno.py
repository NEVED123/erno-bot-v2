import requests as req
from competition import Competition
from bs4 import BeautifulSoup as bs 
import discord
from constants import CHANNEL_ID, TOKEN, COMP_URL, TABLE_NAME
import boto3 as bt

# ---- Adapters to external resources ----

db = bt.client('dynamodb')

def get_all_comps():
    r = req.get(COMP_URL)
    r.encoding = 'ISO-8859-1'
    content = r.content
    soup = bs(content, 'html.parser')
    comp_soups = soup.find_all('li', attrs={'class':'list-group-item not-past'})
    competitions = [Competition(soup=s) for s in comp_soups]
    return competitions

def get_previous_comps():
    db_response = db.scan(TableName=TABLE_NAME)['Items']
    competitions = [Competition(
        name=item['name']['S'], 
        date=item['date']['S'],
        location=item['location']['S'],
        link=item['link']['S']
    ) for item in db_response]
    return competitions
                                  
def record_new_comp(comp: Competition, ):
    db.put_item(
        TableName=TABLE_NAME, 
        Item={
            "name": {"S": comp.name},
            "date": {"S": comp.date},
            "location": {"S": comp.location},
            "link": {"S": comp.link},
        }   
    )

# --- Main logic ---

def get_new_comps() -> list[Competition]:
    all_comps = get_all_comps()
    previous_comps = get_previous_comps()
    new_comps = [comp for comp in all_comps if comp not in previous_comps]
    for comp in new_comps:
        record_new_comp(comp)
    return new_comps

# --- Discord Bot ---

class ErnoBot(discord.Client):
    async def on_ready(self):
        new_comps = get_new_comps()
        if len(new_comps) > 0:
            channel = self.get_channel(CHANNEL_ID)
            for comp in new_comps:
                await channel.send(comp.create_announcement())
        await self.close()

def main():
    intents = discord.Intents.default()
    intents.messages = True
    client = ErnoBot(intents=intents)
    client.run(TOKEN)

def lambda_handler(event, context):
    main()