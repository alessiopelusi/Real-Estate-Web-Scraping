# Real-Estate-Web-Scraping

This Python project provides a solution for scraping real estate listings from a website and managing them in a database. It's designed to help users keep track of new and updated property listings, ensuring that they are aware of the latest opportunities in the real estate market.

● Project Components

1 ● scraper.py

The scraper.py script uses Selenium and ChromeDriver to scrape real estate listings from a specific URL. It retrieves various details of each property listing, such as title, price, room count, area, bathrooms, floor, and description. It also identifies the URL for further reference.

Web scraping using Selenium: Automates the process of navigating to the website, locating property listings, and extracting data.
Deduplication: Eliminates duplicate listings to avoid redundancy.

2 ● main.py

The main.py script is responsible for coordinating the scraping process and managing the listings in a database. It performs the following tasks:
<pre>
Scrapes new listings from the specified URL.
Compares the new listings with those already present in the database to find matches.
Updates existing listings if a match is found.
Inserts new listings into the database if no match is found.
Removes old listings from the database, ensuring it only contains recent data.
This script uses a database to store property listings and maintains data integrity.
</pre>

3 ● database.py

The database.py module handles database interactions. It includes functions for database connection, selecting listings, checking for the existence of a listing, updating listings, and removing old listings.

● How to use

1 ● Ensure you have Python and the required libraries (Selenium, webdriver_manager, and MySQL Connector) installed.

2 ● Set up a MySQL database with the necessary structure for storing property listings. You can customize the database configuration in the database.py file.

3 ● Run the main.py script to start scraping and managing property listings.

4 ● The script will automatically detect new listings, update existing ones, and remove outdated entries from the database.

5 ● For each new listing or updated listing, the script can open the URL in a web browser, allowing you to view the details online.

● Note

The 'main.py' script is specifically tailored to work with real estate listings from the website 'www.immobiliare.it'. It automates the process of scraping and managing property listings from this specific website.

Ensure that your database configuration in database.py matches your MySQL database setup.

This project demonstrates how to automate real estate listing management but can be extended and customized for other use cases.
