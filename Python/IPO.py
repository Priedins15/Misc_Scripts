import requests
from bs4 import BeautifulSoup
import mysql.connector

# Scrape URL
url = "https://www.marketwatch.com/tools/ipo-calendar"
def scrape_and_save_data(table_index, target_table_name):
    # HTTP GET request
    response = requests.get(url)

    # Check Request
    if response.status_code == 200:

        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find_all("table")[table_index]

        data = []

        # Loop through the table
        for row in table.find_all("tr"):
            # Extract the text from each cell
            cell_data = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
            data.append(cell_data)

        # Create a MySQL connection
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="xxxxxxx",
            database="stock_data"
        )

        cursor = connection.cursor()

        # Create the db table
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {target_table_name} (
            company_name VARCHAR(255),
            proposed_symbol VARCHAR(255),
            exchange VARCHAR(255),
            price_range VARCHAR(255),
            shares VARCHAR(255),
            week_of VARCHAR(255)
        );
        '''
        cursor.execute(create_table_query)

        # Delete existing data
        delete_data_query = f'DELETE FROM {target_table_name}'
        cursor.execute(delete_data_query)

        # Insert the scraped data
        insert_data_query = f'INSERT INTO {target_table_name} VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.executemany(insert_data_query, data)

        # Commit changes
        connection.commit()
        connection.close()

        print(f"Data from table {table_index} saved to the {target_table_name} table.")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Call the function to scrape and save data for each table
scrape_and_save_data(0, 'ipohis')
scrape_and_save_data(1, 'ipotw')
scrape_and_save_data(2, 'iponw')
