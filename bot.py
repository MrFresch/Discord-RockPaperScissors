import discord
import random
import mysql.connector
import yaml

with open(R"C:\Users\micro\Documents\SynyxBOGY\Discord_Bot_SSP\config.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

from mysql.connector import connect, Error

activeGames = []
options = ['scissors', 'rock', 'paper']

def insertHighScore(ID, Score):
    records = [(str(ID), Score)]
    try:
        with connect(
            host=cfg["DB"]["host"],
            user=cfg["DB"]["user"],
            password=cfg["DB"]["password"],
        ) as connection:
            query = """INSERT INTO `DiscordBot`.`Highscore`(ID, Score) VALUES (%s, %s)"""
            with connection.cursor() as cursor:
                cursor.executemany(query, records)
                connection.commit()
    except Error as e:
        print(e)

def TriesAndHighscore(ID):
    try:
        with connect(
            host=cfg["DB"]["host"],
            user=cfg["DB"]["user"],
            password=cfg["DB"]["password"],
        ) as connection: 
            query = f"SELECT COUNT(ID) , SUM(Score) FROM DiscordBot.Highscore WHERE ID = '{ID}';"
            print(query)
            with connection.cursor() as cursor:
                cursor.execute(query)
                line = cursor.fetchone()
                print(line)
                return line[0], line[1]
    except Error as e:
        print(e)

def compareStrings(ownPick, playerPick):
    print(ownPick + playerPick)
    if ownPick == playerPick:
        return 0
    if ownPick == "scissors":
        if playerPick == "rock":
            return 1
        if playerPick == "paper":
            return -1
    if ownPick == "rock":
        if playerPick == "paper":
            return 1
        if playerPick == "scissors":
            return -1
    if ownPick == "paper":
        if playerPick == "scissors":
            return 1
        if playerPick == "rock":
            return -1

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.author in activeGames:
            print("lol")
            if message.content in options:
                i = compareStrings(random.choice(options), message.content)
                print(i)
                if i == 0:
                    await message.channel.send("It's a tie!")
                if i == 1:
                    await message.channel.send("You loose! Don't you go sad on me now.")
                if i == -1:
                    await message.channel.send("You won! WOOOHOOOOO! what are you doing with your life playing this.")
                await message.channel.send("Thank you for playing!")
                activeGames.remove(message.author)
                insertHighScore(message.author, i)
            else:
                await message.channel.send("Please pick either \"rock\", \"paper\" or \"scissors\"!")

        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content == '/highscore':
            count,score = TriesAndHighscore(str(message.author))
            await message.channel.send(f"After having played {count} games, you reached a balance (every win and loss added together) of {score}! Congratulations!")
            if score <= 0:
                await message.channel.send("Well, you are pretty damn bad at a game depending completely on chance. Must be a personal thing!")
            if score > 0:
                await message.channel.send("Wow, that's a pretty good score! Look at you being happy about something completely random.")

        if message.content == "/StartRPS":
            activeGames.append(message.author)
            print(activeGames)
            await message.channel.send("The game is starting! Have fun, {}!".format(message.author.name))
            await message.channel.send("Answer with \"rock\", \"paper\" or \"scissors\"!")

client = MyClient()
client.run(cfg["Discord"]["Token"])