


import discord
import re
import os
import pymongo
from bson.objectid import ObjectId
from decouple import config


password = config('DBpassword')
TOKEN = config('counting_TOKEN')
prefix = "$"
DBclient = pymongo.MongoClient(f"mongodb+srv://memo:{password}@counting-bot.bgcgt.mongodb.net/")
db = DBclient.countingBot['counting-bot']


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


current_num = 0
last_user = 928950044823019571
new_streak = False



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="helping with counting under $help"))
    print('We have logged in as {0.user}'.format(client))
    get_val()


def get_val():
    global current_num
    global last_user
    global new_streak
    data = db.find_one({'_id': ObjectId('6239beea1b83f8d2311e27d3')})
    if "current_num" in data:
      current_num = data["current_num"]
    if "last_user" in data:
        last_user = data["last_user"]
    if "new_streak" in data:
        new_streak = data["new_streak"]
def get_high_score():
    data = db.find_one({'_id': ObjectId('6239beea1b83f8d2311e27d3')})
    if "high_score" in data:
        return data["high_score"]
def get_high_score_setter():
    data = db.find_one({'_id': ObjectId('6239beea1b83f8d2311e27d3')})
    if "high_score_setter" in data:
        return data["high_score_setter"]
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
    
    global current_num
    global last_user
    global new_streak

    high_score = get_high_score()
    high_score_setter = get_high_score_setter()

    test_channel = client.get_channel(936978995487076403) #test
    allowed_channel = client.get_channel(905610342703431690) #count
    current_channel = client.get_channel(message.channel.id)
    
    message_content = message.content
    current_user = message.author.id
    secsess = u"\u2705"
    fail = u"\u274C"
    warning = u"\u26A0"
    hund = "💯"
    
    if current_channel == client.get_channel(858117549328564234) and message_content == f"{prefix}get_unpingable":
        
        for role in message.author.roles:
            if(role.name == 'Staff'):
                channel = client.get_channel(984670647017947196)
                members = message.guild.members
                regex = '[\x00-\x7F]'

                for mem in members:
                    if mem.nick != None and not re.search(regex,mem.nick):
                            await channel.send(f'nick: {mem.nick}, id: {mem.id}\n')
                    elif mem.nick == None:
                        if not re.search(regex,mem.name):
                            await channel.send(f'name: {mem.name}, id: {mem.id}\n')
        

    # if current_channel == test_channel and message_content == f"{prefix}remove" and current_user == 264088659295207425:
    #     roles = message.guild.roles
    #     for role in roles:
    #         if(role.name == "testing"):
    #             print("removed")
    #             await message.author.remove_roles(role, atomic=True)
    
    if current_channel == allowed_channel and message_content == f"{prefix}rsb":
        for role in message.author.roles:
            if(role.name == 'Staff'):
                reset_bot()
                await current_channel.send("Reset complete")
    elif current_channel == allowed_channel and message_content == f"{prefix}help":
        embed=discord.Embed(color=0x65b1d2)
        embed.add_field(name="Counting rules: ", value="• One person can't count two numbers in a row. (A friend/partner is required)\n• Can't do math\n • Cannot have any text in the message, only number", inline=False)
        embed.add_field(name="Commands ", value="• $help: Get this help text\n• $rsb: resets the bot (Staff Only)\n • $high_score: shows the current high-score", inline=False)
        await message.author.send(embed=embed)
    elif current_channel == allowed_channel and message_content == f"{prefix}high_score":
        
        user = await message.guild.fetch_member(int(high_score_setter))
        
        if (user.nick != None):
            user_name = user.nick
        else:
            user_name = user.name

        await current_channel.send(f"The current high-score is {high_score} and was set by {user_name}")

    if current_channel == allowed_channel and re.search("\d*",message_content) and not re.search("\D", message_content):
        
        if new_streak == False and int(message_content) != current_num + 1: 
            
            await message.add_reaction(warning)
            await current_channel.send(
                "Incorrect number! The next number is `1`. **No stats have been changed since the current number was 0.**")
        elif last_user != current_user and int(message_content) == current_num + 1:
            new_streak = True
            last_user = current_user
            if int(message_content) == 100:
                await message.add_reaction(hund)
            elif int(message_content) == 69:
                await message.add_reaction("🇳")
                await message.add_reaction("🇮")
                await message.add_reaction("🇨")
                await message.add_reaction("🇪")
            else:
                await message.add_reaction(secsess)
            current_num += 1
            if current_num > high_score:
                high_score = current_num
                old_high_score = high_score_setter
                high_score_setter = current_user
                
                roles = message.guild.roles
                for role in roles:
                    if(role.name == "Highest Counter"):
                        add_user = await message.guild.fetch_member(int(high_score_setter))
                        remove_user = await message.guild.fetch_member(int(old_high_score))
                        await add_user.add_roles(role, atomic=False)
                        await remove_user.remove_roles(role, atomic=False)

        else:
            if last_user == current_user:
                await current_channel.send(message.author.mention + f" RUINED IT AT **{current_num + 1}** !! Next number is **1**. **You can't count two numbers in a row.**")
            else:
                await current_channel.send(message.author.mention + f" RUINED IT AT **{current_num + 1}** !! Next number is **1**. **Wrong number.**")
            await message.add_reaction(fail)
            current_num = 0
            last_user = 928950044823019571
            new_streak = False
        temp_data ={
            'current_num' : int(current_num),
            'last_user' : int(last_user),
            'new_streak' : new_streak,
            'high_score': int(high_score),
            'high_score_setter': int(high_score_setter)
                    }
        update_val(temp_data)
        get_val()
        
    


client.run(TOKEN)

