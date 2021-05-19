import discord
import random
import mysql.connector
import yaml

with open("/home/pi/Documents/DiscordBotRPS/config.yaml", "r") as ymlfile:
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

def checkRegistered(ID):
    try:
        with connect(
            host=cfg["DB"]["host"],
            user=cfg["DB"]["user"],
            password=cfg["DB"]["password"],
        ) as connection: 
            query = f"SELECT COUNT(ID) FROM DiscordBot.Users WHERE ID = '{ID}';"
            print(query)
            with connection.cursor() as cursor:
                cursor.execute(query)
                line = cursor.fetchone()
                print(line)
                return line[0]
    except Error as e:
        print(e)

def checkAllState():
    try:
        with connect(
            host=cfg["DB"]["host"],
            user=cfg["DB"]["user"],
            password=cfg["DB"]["password"],
        ) as connection: 
            query = "SELECT Fair FROM DiscordBot.Users WHERE ID = 'ALL';"
            print(query)
            with connection.cursor() as cursor:
                cursor.execute(query)
                line = cursor.fetchone()
                print(line[0])
                return line[0]
    except Error as e:
        print(e)

def registerInDatabank(ID, fair = True):
    if fair:
        fair = 1
    else:
        fair = 0
    try:
        with connect(
            host=cfg["DB"]["host"],
            user=cfg["DB"]["user"],
            password=cfg["DB"]["password"],
        ) as connection:
            query = f"INSERT INTO `DiscordBot`.`Users`(ID, Fair) VALUES ('{str(ID)}', {fair}) ON DUPLICATE KEY UPDATE fair = {fair}"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
    except Error as e:
        print(e)

def compareStrings(ownPick, playerPick):
    print(ownPick + playerPick)
    if checkAllState() == 0:
        return -1
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
        if message.content == '/sWox':
            registerInDatabank('ALL', 0)
            await message.channel.send("You have successfully changed the Gamemode to unfair.")
            return
        if message.content == '/sWoy':
            registerInDatabank('ALL', 1)
            await message.channel.send("You have successfully changed the Gamemode to fair.")
            return
        if message.channel.id == cfg["Discord"]["Arcade-Channel"]:
            if message.author in activeGames:
                print("lol")
                if message.content in options:
                    compPick = random.choice(options)
                    i = compareStrings(compPick, message.content)
                    print(i)
                    if i == 0:
                        await message.channel.send("It's a tie!")
                        await message.channel.send("I had picked " + message.content + "!")
                    if i == -1:
                        await message.channel.send("You loose! Don't you go sad on me now.")
                        if message.content == 'rock':
                            await message.channel.send("I had picked paper! Paper incapsulates the rock.")
                        if message.content == 'paper':
                            await message.channel.send("I had picked scissors! Scissors cut the paper.")
                        if message.content == 'scissors':
                            await message.channel.send("I had picked rock! Rock smashes the scissors.")
                    if i == 1:
                        await message.channel.send("You won! WOOOHOOOOO! what are you doing with your life playing this.")
                        if message.content == 'rock':
                            await message.channel.send("I had picked scissors! Rock smashes the scissors, good job!")
                            await message.channel.send("Your highscore is going up... Check it out by using /highscore.")
                        if message.content == 'paper':
                            await message.channel.send("I had picked rock! Paper incapsulates the rock, good job!")
                            await message.channel.send("Your highscore is going up... Check it out by using /highscore.")
                        if message.content == 'scissors':
                            await message.channel.send("I had picked paper! Scissors cut the paper, good job!")
                            await message.channel.send("Your highscore is going up... Check it out by using /highscore.")
                    await message.channel.send("Thank you for playing!")
                    activeGames.remove(message.author)
                    insertHighScore(message.author, i)
                    return
                else:
                    await message.channel.send("Please pick either \"rock\", \"paper\" or \"scissors\"!")
                    return

            if message.content == 'ping':
                await message.channel.send('pong')
                return

            if message.content == '/register':
                await message.channel.send('You have been registered! You can now play RPS and get your highscore calculated.')
                registerInDatabank(message.author)
                return
            
            if message.content == '/highscore':
                count,score = TriesAndHighscore(str(message.author))
                await message.channel.send(f"After having played {count} games, you reached a balance (every win and loss added together) of {score}! Congratulations!")
                if score <= 0:
                    await message.channel.send("Well, you are pretty damn bad at a game depending completely on chance. Must be a personal thing!")
                    return
                if score > 0:
                    await message.channel.send("Wow, that's a pretty good score! Look at you being happy about something completely random.")
                    return

            if message.content == "/StartRPS":
                print(activeGames)
                if checkRegistered(message.author) == 0:
                    await message.channel.send("You have to register with /register before being able to play.")
                    return
                else:
                    await message.channel.send("The game is starting! Have fun, {}!".format(message.author.name))
                    await message.channel.send("Answer with \"rock\", \"paper\" or \"scissors\"!")
                    activeGames.append(message.author)
                    return

client = MyClient()
client.run(cfg["Discord"]["Token"])