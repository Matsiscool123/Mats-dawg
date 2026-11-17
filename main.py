import 【entity-discord¦canonical_name=discord】
from 【entity-discord¦canonical_name=discord】.ext import commands
import random
import os
import json
from datetime import date

intents = 【entity-discord¦canonical_name=discord】.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_user(data, user_id):
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "money": 0,
            "total_weight": 0,
            "total_catches": 0,
            "biggest_fish": 0,
            "biggest_fish_name": "None yet",
            "daily_biggest": 0,
            "daily_biggest_name": "None yet",
            "daily_date": str(date.today()),
            "last_daily": ""
        }
    if data[user_id]["daily_date"] != str(date.today()):
        data[user_id]["daily_biggest"] = 0
        data[user_id]["daily_biggest_name"] = "None yet"
        data[user_id]["daily_date"] = str(date.today())
    return data[user_id]

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online als {bot.user}!")

# ---------- LEADERBOARD ALL TIME ----------
@bot.tree.command(name="leaderboard", description="All-time leaderboard - heaviest fishers ever!")
async def leaderboard(interaction: discord.Interaction):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("total_weight", 0), reverse=True)[:10]
    if not sorted_users:
        await interaction.response.send_message("Nobody has fished yet! Be the first with /fish!")
        return
    tekst = "**🏆 ALL-TIME LEADERBOARD - Total Weight** 🏆\n\n"
    medailles = ["🥇", "🥈", "🥉", "4.", "5.", "6.", "7.", "8.", "9.", "10."]
    for i, (user_id, u) in enumerate(sorted_users):
        try:
            member = await interaction.guild.fetch_member(int(user_id))
            naam = member.display_name
        except:
            naam = f"User {user_id}"
        tekst += f"{medailles[i]} **{naam}** - {u.get('total_weight', 0):.2f}kg total | {u.get('total_catches', 0)} fish | Biggest: {u.get('biggest_fish_name')} ({u.get('biggest_fish')}kg)\n"
    await interaction.response.send_message(tekst)

# ---------- DAILY LEADERBOARD - HEAVIEST FISH TODAY ----------
@bot.tree.command(name="daily_leaderboard", description="Daily leaderboard - heaviest fish of today!")
async def daily_leaderboard(interaction: discord.Interaction):
    data = load_data()
    vandaag = str(date.today())
    filtered = []
    for user_id, u in data.items():
        if u.get("daily_date") == vandaag and u.get("daily_biggest", 0) > 0:
            filtered.append((user_id, u))
    filtered = sorted(filtered, key=lambda x: x[1].get("daily_biggest", 0), reverse=True)[:10]
    if not filtered:
        await interaction.response.send_message("Nobody has fished today yet! Be the first with /fish! 🎣")
        return
    tekst = f"**🎣 DAILY LEADERBOARD - Heaviest Fish Today ({vandaag})** 🎣\n\n"
    medailles = ["🥇", "🥈", "🥉", "4.", "5.", "6.", "7.", "8.", "9.", "10."]
    for i, (user_id, u) in enumerate(filtered):
        try:
            member = await interaction.guild.fetch_member(int(user_id))
            naam = member.display_name
        except:
            naam = f"User {user_id}"
        tekst += f"{medailles[i]} **{naam}** - {u.get('daily_biggest_name')} ({u.get('daily_biggest')}kg)\n"
    await interaction.response.send_message(tekst)

# ---------- RICHEST LEADERBOARD - MOST MONEY RIGHT NOW ----------
@bot.tree.command(name="richest", description="Leaderboard - who has the most money right now!")
async def richest(interaction: discord.Interaction):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("money", 0), reverse=True)[:10]
    if not sorted_users:
        await interaction.response.send_message("Nobody has coins yet! Do /fish or /daily!")
        return
    tekst = "**💰 RICHEST LEADERBOARD - Most Money Right Now** 💰\n\n"
    medailles = ["🥇", "🥈", "🥉", "4.", "5.", "6.", "7.", "8.", "9.", "10."]
    for i, (user_id, u) in enumerate(sorted_users):
        try:
            member = await interaction.guild.fetch_member(int(user_id))
            naam = member.display_name
        except:
            naam = f"User {user_id}"
        tekst += f"{medailles[i]} **{naam}** - {u.get('money', 0)} coins 💰\n"
    await interaction.response.send_message(tekst)

bot.run(os.getenv("TOKEN"))
