import mysql.connector
import time
import pymongo
from apscheduler.schedulers.background import BackgroundScheduler
import os

db_config = {
    "host": "player-db",
    "port": 3306,
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

# MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://stats-db:27017/")
mongo_db = mongo_client[os.getenv("MONGO_INITDB_DATABASE")]
stats_collection = mongo_db[os.getenv("MONGO_COLLECTION")]

def store_stats():
    try:
        # Get mysql data
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT id, name, points FROM players")
        players = cursor.fetchall()
        cursor.close()
        conn.close()

        if players:
            # Do calculations
            top_player = max(players, key=lambda player: player["points"])
            worse_player = min(players, key=lambda player: player["points"])
            total_points = sum(player["points"] for player in players)
            average_points = round(total_points / len(players), 1)

            stats = {
                "top_player": top_player,
                "worse_player": worse_player,
                "average_points": average_points,
                "timestamp": time.time()
            }
            stats_collection.insert_one(stats)
            print("Stored stats:", stats)
        else:
            print("No data available, skipping..")

    except mysql.connector.Error as err:
        print(f"Error getting player data: {err}")

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(store_stats, 'interval', seconds=5)
    scheduler.start()

if __name__ == "__main__":
    init_scheduler()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

