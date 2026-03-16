# 🍽️ Restaurant Billing System (Python + MySQL + Tkinter)

A desktop-based Restaurant Billing System built using **Python, Tkinter
GUI, SQLAlchemy ORM, and MySQL database**. This application allows
restaurant staff to manage menu items, create orders, generate bills,
and store billing records in a database.

------------------------------------------------------------------------

# 📌 Features

✔ GUI-based restaurant billing system\
✔ Menu management (Add new items)\
✔ Add items to cart with quantity\
✔ Automatic subtotal, tax, and total calculation\
✔ Generate bill preview\
✔ Save bill to database\
✔ Export bill as `.txt` file\
✔ MySQL database integration using ORM

------------------------------------------------------------------------

# 🛠️ Technologies Used

-   Python
-   Tkinter (GUI)
-   SQLAlchemy (ORM)
-   MySQL
-   PyMySQL
-   Decimal Library (for accurate currency calculation)

------------------------------------------------------------------------

# 📂 Project Structure

restaurant-billing-system

├── billing_app.py \# Main application file\
├── README.md \# Project documentation\
├── requirements.txt \# Python dependencies\
└── bills/ \# Saved bill files

------------------------------------------------------------------------

# ⚙️ Requirements

Install the following before running the project:

-   Python 3.8+
-   MySQL Server
-   pip

Python libraries:

-   sqlalchemy
-   pymysql
-   tkinter

Install dependencies:

pip install sqlalchemy pymysql

------------------------------------------------------------------------

# 🗄️ Database Setup

Create the MySQL database:

CREATE DATABASE pythonclassoops;

Update the database credentials in the code:

DB_CONFIG = { "USERNAME": "Heisenberg", "PASSWORD": "saymyname", "HOST":
"localhost", "DATABASE": "pythonclassoops", }

------------------------------------------------------------------------

# ▶️ How to Run

Run the Python file:

python billing_app.py

The application window will open.

------------------------------------------------------------------------

# 🖥️ Application Workflow

1.  Load menu items from database\
2.  Select menu item\
3.  Add quantity to cart\
4.  View cart details\
5.  Generate bill\
6.  Save bill to database and file

------------------------------------------------------------------------

# 🧾 Example Bill Output

===== RESTAURANT BILL =====\
Date: 2026-03-16 12:30:15\
----------------------------------------\
Burger x2 = 240\
Fries x1 = 90\
----------------------------------------\
Subtotal: 330\
Tax (5%): 16.50\
TOTAL: 346.50\
========================================

------------------------------------------------------------------------

# 🚀 Future Improvements

-   Add bill printing
-   Add PDF bill export
-   Add admin login
-   Add sales report dashboard
-   Add inventory tracking

------------------------------------------------------------------------

# 👨‍💻 Author

**Vigneshwar**\
B.Tech Information Technology\
Aspiring Data Scientist & Software Developer
