import os
import calendar
import asyncio
import time
import dateparser
import datetime

from discord.ext import commands

TOKEN = os.environ["TOKEN"]
bot = commands.Bot(command_prefix="/")


async def background_function():
    await bot.wait_until_ready()
    global reminders
    while not bot.is_closed():
        try:
            print(reminders)
            now = datetime.datetime.fromtimestamp(time.time())
            for (date, channel_id, message, day_of_week) in reminders:
                if (
                    now.hour == date.hour
                    and now.minute == date.minute
                    and (
                        day_of_week == "everyday"
                        or day_of_week.lower() == calendar.day_name[now.weekday()].lower()
                    )
                ):
                    print(f"Sending reminder {message}")
                    channel = bot.get_channel(channel_id)
                    await channel.send(message)
        except:
            print("error")
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    global reminders
    reminders = []
    if os.path.isfile("reminder.csv"):
        print("loading previous configuration")
        with open("reminder.csv", "r") as f:
            for line in f.readlines():
                time, channel_id, message, day_of_week = line.strip().split(",")
                reminders.append((dateparser.parse(time), int(channel_id), message, day_of_week))
    print("bot ready to go")
    print("guilds available ", bot.guilds)


@bot.command(name="daily")
async def remind_daily(ctx):
    await ctx.send("@here bora daily!!!")


@bot.command(
    name="setReminder", help="Set a reminder with /setReminder 'time' 'message' 'day_of_week'"
)
async def set_reminder(ctx, time, message, day_of_week="everyday"):
    global reminders
    # first check if time is a valid time
    try:
        time = dateparser.parse(time)
    except:
        await ctx.send("Wrong date format")
        return
    channel_id = ctx.message.channel.id
    reminders.append((time, channel_id, message, day_of_week))
    with open("reminder.csv", "a") as f:
        f.write(f"{time},{channel_id},{message},{day_of_week}\n")
    await ctx.send("reminder configurado")


bot.loop.create_task(background_function())
bot.run(TOKEN)
