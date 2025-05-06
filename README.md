# Pharmacy Management System

A simple Pharmacy Management System developed as a DBMS project using Python and MySQL. This application provides a GUI to manage pharmaceutical data, including drugs, companies, sales, purchases, and user authentication.

## 🛠 Features

- 🧾 **Login System** – Basic user authentication
- 💊 **Drug Management** – Add, update, and list drugs
- 🏬 **Company Module** – Maintain pharmaceutical companies' data
- 📦 **Purchase & Sales** – Record drug purchases and generate sales bills
- ⚠️ **Stock Warnings** – Alerts for low or finished stock
- 📜 **GUI Interface** – Built-in graphical user interface for ease of use

## 🗂 Project Structure

DBMS Project/
│
├── main.py # Main entry point
├── dbpharma.sql # MySQL database schema
└── gui/
├── login.py # User login GUI
├── Login_Details.py
├── Pharmacy.py
├── Sales_Bill.py
├── Warning.py
├── User.py
├── Drug_List.py
├── all_deals.py
├── Almost_Finish.py
├── company.py
├── Buy_Drug.py
├── connect.py # DB connection config
├── Drug.py
├── Warning_List.py
└── pycache/ # Compiled Python cache files

Setup MySQL Database
Open your MySQL client (phpMyAdmin, MySQL Workbench, etc.)

Import the dbpharma.sql file to create the required schema and tables.
