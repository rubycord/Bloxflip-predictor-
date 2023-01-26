
import discord
import time
from discord import app_commands

import cloudscraper
from discord.ext import commands
import math



class aclient(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.default())
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync()
      self.synced = True
    print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)

scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'ScraperBot/1.0',
        }
    )

@tree.command()
@discord.app_commands.checks.has_role("customers")
async def authlink(interaction: discord.Interaction, auth: str):
  r = scraper.get("https://api.bloxflip.com/user", headers={"x-auth-token": auth}).json()
  if r["success"] == False:
    embed = discord.Embed(title="BloxFlip API Error", description="Invaild Auth", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)
  else:
      if r["success"] == True:
        with open(f"Auths/{interaction.user.id}.txt", "w") as f:
          f.write(auth)
          embed = discord.Embed(title="Success, Connected", color=0x00FF00)
          await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(description="Withdraw")
@discord.app_commands.checks.has_role("customers")
async def withdraw(interaction: discord.Interaction, robux : int):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r = scraper.post('https://api.bloxflip.com/user/withdrawTarget', headers={"x-auth-token": auth},  json={"amount": robux} ).json()
    msg = r["msg"]
    if msg == "The specified amount is greater than your account's balance. Please pick a lower amount of R$ !":
      embed = discord.Embed(title="Error", description="You don't have enough R$", color=discord.Color.red())
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      if robux == 1 or robux == 2 or robux == 3 or robux == 4 or robux == 5 or robux == 6 or robux == 7 or robux == 8 or robux == 9 or robux == 0:
        embed = discord.Embed(title="Not Right Amount", description="Please Enter A Vaild Amount", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
      else:
        embed = discord.Embed(title="Success", description="Withdrawed Successfully", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)


@tree.command(description="Deposit")
@discord.app_commands.checks.has_role("customers")
async def deposit(interaction: discord.Interaction, robux : int):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r = scraper.post('https://api.bloxflip.com/user/liquidate', headers={"x-auth-token": auth},  json={"amount": robux} ).json()
    msg = r["msg"]
    if msg == "The liquidation process has started. It may take some time for your R$ to be transferred to your BloxFlip balance!":
      embed = discord.Embed(title="Success", description="Liquidation Started Successfully, (Buggy Command)", color=discord.Color.green())
      await interaction.response.send_message(embed=embed)
import asyncpraw
import random
import json
import urllib


@tree.command(description="Guess The Number, 534-1246, Win Lifetime")
async def guess(interaction: discord.Interaction, number: int):
  x = random.randint(534, 1246)
  if x == number:
    embed = discord.Embed(title="Success", description="You guessed the number correctly", color=discord.Color.green())
    embed.add_field(name="Your Guess", value=str(number))
    embed.set_footer(text="DM me for proof")
    await interaction.response.send_message(embed=embed)
  else:
    embed = discord.Embed(title="Wrong Guess", description="You guessed the number incorrectly", color=discord.Color.red())
    embed.add_field(name=f"Your Guess: {number}\n Correct: {x}", value=str(number))
    embed.set_footer(text="❌")
    await interaction.response.send_message(embed=embed)
#Auto Mines :)  



@tree.command(description="Cashout")
@discord.app_commands.checks.has_role("customers")
async def cashout(interaction: discord.Interaction):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r= scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth}, json={"cashout": True}).json()
    embed = discord.Embed(title="Success", description="Mines Cashed Successfully", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

    r2 = scraper.get('https://api.bloxflip.com/games/mines', headers={"x-auth-token": auth}).json()
    if r2["hasGame"] == False:
      embed = discord.Embed(title="Please Start A Game", description="Now", color=discord.Color.red())
      await interaction.edit_original_response(embed=embed)
    

@tree.command(description="Claim Your Affilate")
@discord.app_commands.checks.has_role("customers")
async def claim(interaction: discord.Interaction, amount : int):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r = scraper.post('https://rest-bf.blox.land/user/affiliates/claim', headers={
									"x-auth-token": auth
								}, json={
									"amount": str(amount)
								}).json()
    checkrobux = r["msg"]
    if checkrobux == "You must have collected at least 100R$ before claiming them!":
      embed = discord.Embed(title="You Must Collect 100R$ Before Claiming", description="Please Collect 100R$", color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
    else:
      embed = discord.Embed(title="Success", description="You Claimed Successfully", color=discord.Color.green())
      await interaction.response.send_message(embed=embed)
      
@tree.command(description="Deposit From Bloxland")
async def bloxlanddeposit(interaction: discord.Interaction, amount : int):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r2  = scraper.post('https://rest-bf.blox.land/user/bloxLandDeposit', headers={"x-auth-token": auth}, json={"amount": amount}).json()
    if r2["success"] == True:
      embed = discord.Embed(title="Success", description="Deposited Successfully", color=discord.Color.green())
      await interaction.response.send_message(embed=embed)
    else:
      if r2["success"] == False:
        embed = discord.Embed(title="Error", description="Deposit Failed", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)


@tree.command(description="Check Your Bloxflip Account Info")
@discord.app_commands.checks.has_role("customers")
async def account(interaction: discord.Interaction):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r = scraper.get('https://api.bloxflip.com/user', headers={"x-auth-token": auth}).json()
    wallet = r["user"]["wallet"]
    robloxUsername = r["user"]["robloxUsername"]
    robloxId = r["user"]["robloxId"]
    embed = discord.Embed(title="Bloxflip Account Info", description="Your Bloxflip Account Info", color=discord.Color.green())
    embed.add_field(name="Stats", value=f"{wallet : 2f} R$\nUser: {robloxUsername}\nID: {robloxId}", inline=True)
    await interaction.response.send_message(embed=embed)


    

@tree.command(description="Open Reward Case")
@discord.app_commands.checks.has_role("customers")
@app_commands.choices(choices=[
  app_commands.Choice(name="5-robux", value="1"),
  app_commands.Choice(name="10-robux", value="2"),
  app_commands.Choice(name="25-robux", value="3"),
    app_commands.Choice(name="50-robux", value="4"),
    app_commands.Choice(name="100-robux", value="5")
    ])
async def reward(interaction: discord.Interaction, choices: app_commands.Choice[str]):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r123 = scraper.post('https://api.bloxflip.com/rewards/roll', headers={"x-auth-token": auth}, json={"slug": "5-robux"}).json() 
    checkmessage = r123["msg"]
    if checkmessage == "You need to deposit at least 1 robux before you can open reward cases!":
      embed = discord.Embed(title="You Need To Deposit At Least 1 Robux Before You Can Open Reward Cases", description="Please Deposit 1 Robux Before You Can Open Reward Cases", color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
    else:
      if checkmessage == "This case has already been claimed. Check back later!":
        embed = discord.Embed(title="This Reward Case Has Already Been Claimed", description="Wait Twenty Four Hours To Reopen", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
      else:
        if choices.value == "1":
          r = scraper.post('https://api.bloxflip.com/rewards/roll', headers={"x-auth-token": auth}, json={"slug": "5-robux"}).json()
          embed = discord.Embed(title="Success", description="You have successfully opened the reward case", color=discord.Color.green())
          await interaction.response.send_message(embed=embed)
        else:
          if choices.value == "2":
            rr = scraper.post('https://api.bloxflip.com/rewards/roll', headers={"x-auth-token": auth}, json={"slug": "10-robux"}).json()
            embed = discord.Embed(title="Success", description="You have successfully opened the reward case", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
          else:
            if choices.value == "3":
              rrr = scraper.post('https://api.bloxflip.com/rewards/roll', headers={"x-auth-token": auth}, json={"slug": "25-robux"}).json()
            else:
              if choices.value == "4":
                rrrr = scraper.post('https://api.bloxflip.com/rewards/roll', headers={"x-auth-token": auth}, json={"slug": "50-robux"}).json()
              else:
                if choices.value == "5":
                  rrrrrrrr = scraper.post('https://api.bloxflip.com/rewards/roll', headers={"x-auth-token": auth}, json={"slug": "100-robux"}).json()
                  embed = discord.Embed(title="Success", description="You have successfully opened the reward case", color=discord.Color.green())
                  await interaction.response.send_message(embed=embed)
          
@tree.command()
@commands.guild_only()
@discord.app_commands.checks.has_role("customers")
async def beg(interaction: discord.Interaction, begamount : int, username : str):
  embed = discord.Embed(title="Begging Alert", color=discord.Color.green())
  embed.add_field(name="Begging Info", value=f"User {username} is begging for {begamount} robux!")
  await interaction.response.send_message(embed=embed)



@tree.command()
@discord.app_commands.checks.has_role("customers")
async def crash(interaction: discord.Interaction):
  r = scraper.get("https://rest-bf.blox.land/games/crash").json()
  e = discord.Embed(title="Grabbing API...", color=discord.Color.green())
  await interaction.response.send_message(embed=e)
  time.sleep(1)
  history = r["history"]
  a =  [float(crashpoint["crashPoint"]) for crashpoint in history][::-1][-30:]
  predict=(sum(a)/30)
  e2 = discord.Embed(title=f"Prediction: {predict : .2f}", color=discord.Color.green())
  await interaction.edit_original_response(embed=e2)
from websocket import create_connection


@tree.command()
@discord.app_commands.checks.has_role("customers")
async def crash2(interaction: discord.Interaction, bet : int):
  with open(f"Auths/{interaction.user.id}.txt", "r") as f:
    auth = f.read()
    r = scraper.get("https://api.bloxflip.com/games/crash").json()
    if r['current']['status'] != 2:
      embed = discord.Embed(title="Please Wait, Current Crash In Progress", color=discord.Color.red())
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      ws = create_connection('wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket',header={
        'Sec-WebSocket-Key': 'pPdhX6P/x8ZRc/lPDrNKqA==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    })
      ws.send('40/crash,')
      ws.send(f'42/crash,["auth","{auth}"]')
      history = r["history"]
    bigblackcock =  [float(crashpoint["crashPoint"]) for crashpoint in history][::-1][-30:]
    autocrashprediction=(sum(bigblackcock)/30)
    ws.send('42/crash,'+json.dumps(
        ["join-game",
            {
                "autoCashoutPoint":autocrashprediction,
                "betAmount": bet
            }
    ]))
    embed = discord.Embed(title=f"Joined", description=f"Sucessfully Joined Crash! Predicton: {autocrashprediction : .2f}", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
      
#280

    
  
#345



@tree.command(name="automines")
@discord.app_commands.checks.has_role("customers")
async def automines(interaction: discord.Interaction, mines : int, robux : int, spots : int):
  embed = discord.Embed(title="Remaking ", color=discord.Color.green())
  embed.add_field(name="Remaking", value=f"Mines: {mines} Robux: {robux} Spots: {spots}")
  await interaction.response.send_message(embed=embed)
@tree.command(name="help") 
@discord.app_commands.checks.has_role("customers")
async def help(interaction: discord.Interaction):
  embed = discord.Embed(title="Help", color=discord.Color.blue())
  embed.add_field(name="Commands", value="/account - Check Your Bloxflip Account\n/authlink - Link Bloxflip Account\n/autocase - Create a case game (soon)\n/automines - Auto Mines For Bloxflip\n/beg - Beg For Robux\n/bloxlanddeposit - Deposit From Bloxland\n /cashout - For Auto Mines\n/claim - Claim Your Bloxflip Affiliate\n/clientmines - Create A Mines session but you choose where to click\n/crash - Predict Crash On Bloxflip\n/crash2 - Auto Play Crash From Bot\n/deposit - Deposit From Bloxflip\n/guess - Guess The Number Lifetimr\n/reward - Opens Your Bloxflip Reward Case\n/withdraw - Withdraw From Bloxflip\n/roulette - Predict Roulette On Bloxflip\n/mines1 - Precict Mines On Bloxflip\n/client-towers - Play Towers On Bloxflip As A Client")
  await interaction.response.send_message(embed=embed)

import datetime 
@tree.command()
@discord.app_commands.checks.has_role("customers")
async def roulette(interaction: discord.Interaction):
  currentid = scraper.get("https://api.bloxflip.com/games/roulette").json()["current"]["_id"]
  first = scraper.get("https://api.bloxflip.com/games/roulette").json()["history"][0]["winningColor"]
  second = scraper.get("https://api.bloxflip.com/games/roulette").json()["history"][0]["winningColor"]
  thrid = scraper.get("https://api.bloxflip.com/games/roulette").json()["history"][0]["winningColor"]
  count = first, second, thrid
  redcount = count.count("red")
  pcount = count.count("purple")
  ycount = count.count("yellow")
  redcountt = 100 - (redcount * 25)
  pcountt = 100 - (pcount * 25)
  ycountt = 100 - (ycount * 25)
  if redcountt > pcountt:
    guess = "Red"
  else:
    if pcountt > redcountt:
      guess = "Purple"
    else:
      if ycountt > pcountt:
        guess = "Yellow"
      else:
        guess = "None"
  if redcount == 3:
    streak = "3 Win Streak On Red"
  else:
    if pcount == 3:
      streak = "3 Win Streak On Purple"
    else:
      if ycount == 3:
        streak = "3 Win Streak On Yellow"
      else:
        streak = "No Win Streak"
  embed = discord.Embed(title="Predict Roulette", color=discord.Color.blue())
  embed.add_field(name="Game Info", value=f"Round ID: {currentid}")
  embed.add_field(name=f"Prediction: {guess}\nStreak: {streak}", value=f"\a")
  await interaction.response.send_message(embed=embed)
  

#323

class MyView(discord.ui.View):
    def __init__(self, author):
      self.author = author
      super().__init__()
      async def interaction_check(self, button, interaction):
        return interaction.user.id == self.author.id
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def one(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 0}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
          await interaction.response.edit_message(view=self)

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def three(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 1}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
          await interaction.response.edit_message(view=self)
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def four(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 2}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def five(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 3}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def six(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 4}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def seven(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 4}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def eight(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 5}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)      
        else:
          button.disabled = True
          button.label = "✅"

      
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def nine(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 6}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"


    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def ten(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 7}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def eleven(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 8}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"


    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def twelve(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 9}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def thirteen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 10}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def fourteen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 11}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def fifteen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 12}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def sixteen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 13}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def seventeen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 14}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def eighteen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 15}).json()
        await interaction.response.edit_message(view=self)
        r2 = scraper.post('https://api.bloxflip.com/games/mines').json()
        if r2["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def nineteen(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 16}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def twenty(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 17}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def twentyone(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 18}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def twentytwo(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 19}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def fuck(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 20}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def fucku(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 21}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def fic(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 22}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary) # or .primary
    async def fucksksk(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/mines/action', headers={"x-auth-token": auth},json={"cashout": False, "mine": 23}).json()
        await interaction.response.edit_message(view=self)
        if r["exploded"] == True:
          button.label = "💣"
          button.disabled = True
          for child in self.children:
            child.disabled = True
          await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "✅"
#728
@tree.command()
@discord.app_commands.checks.has_role("customers")
async def clientmines(interaction: discord.Interaction, bet : int, mines : int):
  with open(f"Auths/{interaction.user.id}.txt") as f:
    auth = f.read()
    r = scraper.post('https://api.bloxflip.com/games/mines/create', headers={"x-auth-token": auth}, json={"betAmount": bet, "mines": mines, "cashout": False,
                                                                                                         }).json()
    view = MyView(interaction.user)
    r = scraper.get("https://api.bloxflip.com/games/mines", headers={"x-auth-token": auth}).json()
    mines = r["game"]["minesAmount"]
    bet = r["game"]["betAmount"]
    uuid = r["game"]["uuid"]
    embed = discord.Embed(title="Game Data", description=f"Mines: {mines}\nBet: {bet}\nGame ID: {uuid}", color=discord.Color.red())
    await interaction.response.send_message(view=view, embed=embed)

class Towers(discord.ui.View):
    def __init__(self, author):
      self.author = author
      super().__init__()
      async def interaction_check(self, button, interaction):
        return interaction.user.id == self.author.id
    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary, row=1) # or .primary
    async def towers1(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/towers/action', headers={"x-auth-token": auth},json={"cashout": False, "tile": 1}).json()
        await interaction.response.edit_message(view=self)
        button.label = "💣"
        if r["exploded"] == True:
          button.disabled = True
          for child in self.children:
            child.disabled = True
            button.label = "💣"
            await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "⭐️"
          await interaction.response.edit_message(view=self)

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary, row=1) # or .primary
    async def towers3(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/towers/action', headers={"x-auth-token": auth},json={"cashout": False, "tile": 2}).json()
        await interaction.response.edit_message(view=self)
        button.label = "💣"
        if r["exploded"] == True:
          button.disabled = True
          for child in self.children:
            child.disabled = True
            button.label = "💣"
            await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "⭐️"
          await interaction.response.edit_message(view=self)         

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary, row=1) # or .primary
    async def towersfour(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/towers/action', headers={"x-auth-token": auth},json={"cashout": False, "tile": 3}).json()
        await interaction.response.edit_message(view=self)
        button.label = "💣"
        if r["exploded"] == True:
          button.disabled = True
          for child in self.children:
            child.disabled = True
            button.label = "💣"
            await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "⭐️"
          await interaction.response.edit_message(view=self)

    @discord.ui.button(label="❌",style=discord.ButtonStyle.secondary, row=2) # or .primary
    async def towersfive(self, interaction, button):
      with open(f"Auths/{self.author.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post('https://api.bloxflip.com/games/towers/action', headers={"x-auth-token": auth},json={"cashout": False, "tile": 4}).json()
        await interaction.response.edit_message(view=self)
        button.label = "💣"
        if r["exploded"] == True:
          button.disabled = True
          for child in self.children:
            child.disabled = True
            button.label = "💣"
            await interaction.response.edit_message(view=self)
        else:
          button.disabled = True
          button.label = "⭐️"
          await interaction.response.edit_message(view=self)


@tree.command(name="client-towers")
@discord.app_commands.checks.has_role("customers")
@app_commands.choices(mode=[
  app_commands.Choice(name='Easy', value="Easy"),
  app_commands.Choice(name='Normal', value="Normal"),
  app_commands.Choice(name='Hard', value="Hard")
])
@discord.app_commands.checks.has_role("customers")
async def clientt(interaction: discord.Interaction, mode: app_commands.Choice[str], bet : int):
  if bet == 0 or bet < 5:
    embed = discord.Embed(title="You must bet at least 5 robux.", color=discord.Color.red())
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    if mode.value == "Easy":
      view = Towers(interaction.user)
      with open(f"Auths/{interaction.user.id}.txt", "r") as f:
        auth = f.read()
        r = scraper.post("https://rest-bf.blox.land/games/towers/create", headers={
                        "x-auth-token" :auth
                    },
                    json={
                        "betAmount": str(bet),
                        "difficulty": "easy"
                    }
                )
      embed = discord.Embed(title="We Recommed You Do Not Use This Command Until Fully Done | Love Project SpongeBob | Made By a young kid", color=discord.Color.blue())
      await interaction.response.send_message(view=view, embed=embed)

  




@clientmines.error
async def njjjj(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@automines.error
async def djdjwdkslworhdjakkejrnd(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


    
@clientt.error
async def gyuu(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)




@clientmines.error
async def ygvgughub(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@help.error
async def gguuu(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@bloxlanddeposit.error
async def bybtygvgughub(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@deposit.error
async def oiniinuhiuygvgughub(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@withdraw.error
async def djiwofhsjfoibsodudbskfjithdraw(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@reward.error
async def rewarderror(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@authlink.error
async def aerror(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@account.error
async def accounterror(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@roulette.error
async def rerror(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@claim.error
async def dhekvuufjdkekfjwkwlduidje(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@roulette.error
async def qwfguyqwtgfyuiqwuoiduqwfioyeriugyq(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@crash2.error
async def qwdqwdqwdqwdqwdwrgqwedfwrgefwew(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@crash.error
async def cerror(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)


@roulette.error
async def fhqfew(interaction: discord.Interaction, error):
  if isinstance(error, commands.NoPrivateMessage):
    embed = discord.Embed(title="Error | Command Cant Be Used Here!",color=discord.Color.red())
    await interaction.response.send_message(embed=embed)





from flask import Flask
from threading import Thread
app=Flask("")

@app.route("/")
def index():
    return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()

client.run("yourtoken")

#1000


