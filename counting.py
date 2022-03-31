
import discord
import re
import os
import pymongo
from bson.objectid import ObjectId
from decouple import config
import time


password = config('DBpassword')
TOKEN = config('counting_TOKEN')

DBclient = pymongo.MongoClient(f"mongodb+srv://memo:{password}@counting-bot.bgcgt.mongodb.net/")
db = DBclient.countingBot['counting-bot']



client = discord.Client()
current_num = 0
last_user = 928950044823019571
new_streak = False


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="counting"))
    print('We have logged in as {0.user}'.format(client))
    get_val()


def get_val():
    global current_num
    global last_user
    global new_streak
    data = db.find_one({'_id': ObjectId('6239beea1b83f8d2311e27d3')})
    if("current_num" in data):
      current_num = data["current_num"]
    if("last_user" in data):
        last_user = data["last_user"]
    if ("new_streak" in data):
        new_streak = data["new_streak"]
    
def update_val(vals):
        db.update_one({'_id': ObjectId('6239beea1b83f8d2311e27d3')},{ "$set":  vals })

def reset_bot():
    global current_num
    global last_user
    global new_streak

    current_num = 0
    last_user = 928950044823019571
    new_streak = False
    temp_data ={
    'current_num' : int(current_num),
    'last_user' : int(last_user),
    'new_streak' : new_streak
    }
    update_val(temp_data)
    get_val()

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    print(message)
    global current_num
    global last_user
    global new_streak
    
    allowed_channel = client.get_channel(936978995487076403) #test
    #allowed_channel = client.get_channel(905610342703431690) #count
    current_channel = client.get_channel(message.channel.id)
    
    message_content = message.content
    current_user = message.author.id
    secsess = u"\u2705"
    fail = u"\u274C"
    warning = u"\u26A0"
    hund = "💯"
    if(current_channel == allowed_channel and message_content == "rsb"):
        for role in message.author.roles:
            if(role.name == 'Staff'):
                reset_bot()
                await current_channel.send("Reset complete")
        
    if (current_channel == allowed_channel and re.search("^\d",message_content) and not re.search("/D", message_content)):
        if (new_streak == False and int(message_content) != current_num + 1):
            
            await message.add_reaction(warning)
            await current_channel.send(
                "Incorrect number! The next number is `1`. **No stats have been changed since the current number was 0.**"
                .format(num=current_num + 1))
        elif (last_user != current_user
              and int(message_content) == current_num + 1):
            new_streak = True
            last_user = current_user
            if (int(message_content) == 100):
                await message.add_reaction(hund)
            elif (int(message_content) == 69):
                await message.add_reaction("🇳")
                await message.add_reaction("🇮")
                await message.add_reaction("🇨")
                await message.add_reaction("🇪")
            else:
                await message.add_reaction(secsess)
            current_num += 1
        else:
            if (last_user == current_user):
                await current_channel.send(
                    message.author.mention +
                    " RUINED IT AT **{num}** !! Next number is **1**. **You can't count two numbers in a row.**"
                    .format(num=current_num + 1))
            else:
                await current_channel.send(
                    message.author.mention +
                    " RUINED IT AT **{num}** !! Next number is **1**. **Wrong number.**"
                    .format(num=current_num + 1))
            await message.add_reaction(fail)
            current_num = 0
            last_user = 928950044823019571
            new_streak = False
        temp_data ={
            'current_num' : int(current_num),
            'last_user' : int(last_user),
            'new_streak' : new_streak
                        }
        update_val(temp_data)
        get_val()
        time.sleep(1)
    


client.run(TOKEN)

