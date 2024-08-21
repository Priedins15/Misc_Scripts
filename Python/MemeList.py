import requests
import mysql.connector
from datetime import datetime
from mysql.connector import Error

# Connect to db
def establish_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="xxxxxxx",
            database="crypto"
        )
        return connection
    except Error as err:
        print(f"Error: {err}")
        return None

# Create a table
def create_table(connection):
    cursor = connection.cursor()
    try:
        query = """
            CREATE TABLE IF NOT EXISTS meme_tokens (
                id VARCHAR(255) PRIMARY KEY,
                symbol VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                current_price DECIMAL(18, 8),
                market_cap BIGINT,
                market_cap_rank INT,
                fully_diluted_valuation BIGINT,
                total_volume BIGINT,
                high_24h DECIMAL(18, 8),
                low_24h DECIMAL(18, 8),
                price_change_24h DECIMAL(18, 8),
                price_change_percentage_24h DECIMAL(18, 8),
                market_cap_change_24h BIGINT,
                market_cap_change_percentage_24h DECIMAL(18, 10),
                circulating_supply DOUBLE,
                total_supply DOUBLE,
                max_supply DOUBLE,
                ath DECIMAL(18, 8),
                ath_change_percentage DECIMAL(18, 8),
                ath_date DATETIME,
                atl DECIMAL(18, 8),
                atl_change_percentage DOUBLE,
                atl_date DATETIME,
                last_updated DATETIME,
                INDEX (market_cap_rank)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
        cursor.execute(query)
        connection.commit()
        print("Table created successfully.")
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Insert data into the db
def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        query = """
            REPLACE INTO meme_tokens (
                id, symbol, name, current_price,
                market_cap, market_cap_rank, fully_diluted_valuation,
                total_volume, high_24h, low_24h, price_change_24h,
                price_change_percentage_24h, market_cap_change_24h,
                market_cap_change_percentage_24h, circulating_supply,
                total_supply, max_supply, ath, ath_change_percentage,
                ath_date, atl, atl_change_percentage, atl_date,
                last_updated
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Extract data from the CoinGecko API
        for entry in data:
            if entry['market_cap'] != 0:
                try:
                    values = (
                        entry['id'], entry['symbol'], entry['name'],
                        entry['current_price'], entry['market_cap'], entry['market_cap_rank'],
                        entry['fully_diluted_valuation'], entry['total_volume'], entry['high_24h'],
                        entry['low_24h'], entry['price_change_24h'], entry['price_change_percentage_24h'],
                        entry['market_cap_change_24h'], entry['market_cap_change_percentage_24h'],
                        entry['circulating_supply'], entry['total_supply'], entry['max_supply'],
                        entry['ath'], entry['ath_change_percentage'],
                        datetime.strptime(entry['ath_date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"),
                        entry['atl'], entry['atl_change_percentage'],
                        datetime.strptime(entry['atl_date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"),
                        datetime.strptime(entry['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                    )
                    cursor.execute(query, values)
                except ValueError as e:
                    print(f"Skipping entry with invalid datetime value: {e}")
        connection.commit()
        print("Data inserted or replaced successfully.")
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()



# Main code
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=meme-token&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Connection to the db
    connection = establish_connection()

    if connection:
        # Create a table
        create_table(connection)

        # Insert data
        insert_data(connection, data)

        # Close the db
        connection.close()
else:
    print(f"Error: {response.status_code}")
    print(response.text)