Finance Manager
This is a basic expense tracker built with Python. It uses a desktop interface to log spending and saves everything to a local MySQL database.

What it does
Logs expenses under food, travel, or other categories.

Keeps a running balance in a separate database table so it's consistent.

Lets you search for past entries by a specific date.

Calculates monthly totals so you can see where the money went.

Uses a dark theme because it's easier on the eyes.

Requirements
You'll need these installed:

Python 3.x

CustomTkinter

MySQL Connector

Python-dotenv (for the database password)

How to set it up
Database: You need a MySQL server running. Create a database named expenseTracker. The script handles the table creation for you.

Environment Variables: Create a file named .env in the main folder. Put your MySQL password in there like this: PASSWORD_DB=yourpassword.

Run it: Just run python financeManagerMain.py.

Files
financeManagerMain.py: The main script.

.env: Where the DB password lives (don't push this to git).

.gitignore: Keeps the junk out of the repo.

requirements.txt: List of modules to install.
