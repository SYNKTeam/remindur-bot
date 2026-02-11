# imports for this to work, remove these and I will laugh at you since the bot won't work
import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import aiofiles
import json
import os
import datetime
import re

# this is where we store the user's reminders (you can change this to either SQL based database or something like mongo, or whatever really it's up to you)
STORE_FILE = './store.json'
TOKEN = 'Put your bot token here' # realistically the token should go in a .env but since I'm lazy and cannot be arsed I'm putting it here
PREFIX = 'r.' # prefix for legacy "prefixed" commands

client = commands.Bot(command_prefix = commands.when_mentioned_or(PREFIX), intents = discord.Intents.all()) # note: for intents to work, you need to enable all of the "Privileged Gateway Intents"

async def writeFile(reminders):
    async with aiofiles.open(STORE_FILE, 'w') as file:
        await file.write(json.dumps(reminders, indent = 4)) # self explanatory of what this does
    
@tasks.loop(seconds = 1) # run this func every second
async def checkReminders():
    async with aiofiles.open(STORE_FILE, 'r') as file:
        content = await file.read() # reads everything from the file
        reminders = json.loads(content) # parses the JSON in the file for easier use later
    
    if not reminders:
        return

    now = datetime.datetime.now(datetime.timezone.utc) # current time in UTC

    for reminder in reminders:
        time = datetime.datetime.fromisoformat(reminder['timeToRemind']) # converts the reminder time from ISO format to datetime

        if now >= time: # if the time for the reminder is equal or past, then run the following
            user = await client.fetch_user(reminder['user']) # get the user via the stored userid and store it under user to make sending messages easier
            customEmoji = '<:clock:1465088597840498830>' # make sure to replace this with your custom emoji ID or just use a default emoji, up to you
            discordTimestamp = f'<t:{int(time.timestamp())}:F>' # converts to a unix timestamp so we can use discord's time system to display it in the users local time
            reason = reminder['reason']

            await user.send(f'{customEmoji} Reminder time!!!! You set a reminder for {discordTimestamp} for {reason}.')

            reminders.remove(reminder) # removes the reminder from the list of reminders
            await writeFile(reminders) # calls the func to write to file to delete the old reminder

@client.event
async def on_ready(): # after the bot has actually started
    checkReminders.start() # start the loop

    try:
        commands = await client.tree.sync() # syncs the slash commands ("app commands") with discord
        print(f'Sucessfully loaded {len(commands)} commands!')
    except Exception as e:
        raise e # prints error to console

    print('Bot is now ready!')

def parseInput(input: str) -> datetime.timedelta: # func to parse the time into usable format
    time_regex = re.compile(r'(\d+)\s*([smhdw])') 
    matches = time_regex.findall(input.lower())
    
    delta = datetime.timedelta()
    
    for value, unit in matches:
        value = int(value)
    
        if unit == 's':
            delta += datetime.timedelta(seconds=value)
    
        elif unit == 'm':
            delta += datetime.timedelta(minutes=value)
    
        elif unit == 'h':
            delta += datetime.timedelta(hours=value)
    
        elif unit == 'd':
            delta += datetime.timedelta(days=value)
    
        elif unit == 'w':
            delta += datetime.timedelta(weeks=value)

    return delta

@client.hybrid_command(name = 'remind', description = 'Set\'s a reminder for the specified time with a reason (optional).') # hybrid commands are legacy prefixed commands and slash commands in one function
@app_commands.describe(time = 'The time for when you want to be reminded. Time must be something like: 1h, 2d, 1w, etc.') 
@app_commands.describe(reason = 'The reason for the reminder, optional.')
async def remind(ctx: commands.Context, time: str, *, reason: str = None):
    try:
        reason = reason if reason else 'No reason provided'
        duration = parseInput(time) # parse the provided time using the func we made earlier
        remindTime = datetime.datetime.now(datetime.timezone.utc) + duration # set the remind time to be the time now + the time the user wants to be reminded at

        async with aiofiles.open(STORE_FILE, 'r') as file:
            content = await file.read() # reads the file so when we write to the file previous reminders aren't deleted
            reminders = json.loads(content)

        reminder = {
            'user': ctx.author.id,
            'reason': reason,
            'timeToRemind': remindTime.isoformat()
        }
        reminders.append(reminder) # add to the list of reminders

        await writeFile(reminders) # self explanatory, write to the reminders file

        timestamp = int(remindTime.timestamp())
        await ctx.send(f'Reminder has been set for <t:{timestamp}:R> (<t:{timestamp}:F>) with a reason of: {reason}.') # confirm the reminder has been set
    
    except Exception as e:
        await ctx.send('Oops! There was an error running this command, please make sure you have followed the format for the time. You must provide a time such as "1d", "1w", etc.') # something fucked up and now you're gonna have to troubleshoot :D
        # raise e // if something goes to shit, remove the "#" and this text to enable a more clearer log

client.run(TOKEN) # start the bot with the provided token
