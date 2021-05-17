import mysql.connector

from mysql.connector import connect, Error

try:
    with connect(
        host="raspberrypi",
        user='root',
        password='cA9^xU2Bu&D#Rf',
    ) as connection:
        query = """INSERT INTO `DiscordBot`.`Highscore`(ID, Score) VALUES ('test2', 0);"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
except Error as e:
    print(e)

    
try:
    with connect(
        host="raspberrypi",
        user='root',
        password='cA9^xU2Bu&D#Rf',
    ) as connection:
        query = 'SELECT * FROM `DiscordBot`.`Highscore` LIMIT 1000;'
        with connection.cursor() as cursor:
            cursor.execute(query)
            for line in cursor:
                print(line[2])
except Error as e:
    print(e)


ID = 'test2'
try:
    with connect(
        host="raspberrypi",
        user='root',
        password='cA9^xU2Bu&D#Rf',
    ) as connection: 
        query = f"SELECT COUNT(ID) FROM DiscordBot.Highscore WHERE ID = '{ID}';"
        print(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            for line in cursor:
                print(line[0])
except Error as e:
    print(e)


ID = 'test2'
try:
    with connect(
        host="raspberrypi",
        user='root',
        password='cA9^xU2Bu&D#Rf',
    ) as connection: 
        query = f"SELECT SUM(Score) FROM DiscordBot.Highscore WHERE ID = '{ID}';"
        print(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            for line in cursor:
                print(line[0])
except Error as e:
    print(e)