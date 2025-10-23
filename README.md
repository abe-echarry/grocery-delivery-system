# Grocery Delivery System

**Author:** Abe Echarry  
**Course Project:** [Your Course Name / Code Here]  
**Demo:** [Coming soon – add YouTube or Google Drive link]  
**GitHub Repository:** https://github.com/abe-echarry/grocery-delivery-system  

---

## 🛒 Overview
The **Grocery Delivery System** is a web-based application designed to improve food access in **food deserts** — areas where residents have limited access to fresh, affordable groceries.  
This system allows users to browse grocery items, add them to a cart, and complete secure checkouts for home delivery.  
It’s built with **Python** and **Django**, emphasizing simplicity, accessibility, and reliability for both customers and local vendors.

---

## 💡 Problem Statement
Many communities lack nearby grocery stores, forcing residents to travel long distances for basic necessities.  
This project helps bridge that gap by connecting customers with local markets through a simple web platform that handles product browsing, ordering, and delivery management.

---

## ⚙️ Features
- **User Accounts:** Register, log in, and manage personal profiles.  
- **Product Catalog:** Displays grocery items with details and prices.  
- **Cart and Checkout:** Add, edit, and confirm grocery orders.  
- **Order History:** Keeps records of past purchases for easy reordering.  
- **Admin Panel:** Allows store managers to manage inventory and orders.  
- **Responsive Layout:** Works smoothly on both desktop and mobile devices.

---

## 🧰 Tech Stack
| Component | Technology |
|------------|-------------|
| Backend | Django 5.0 (Python 3.12) |
| Frontend | HTML5, CSS3, Django Templates |
| Database | SQLite (development) / MySQL (optional) |
| Tools | Git, GitHub, Virtual Environment (.venv) |

## 🧱 System Architecture
[ User Interface ]
↓
(HTML / CSS / Django Templates)
↓
[ Django Backend ]
(Handles authentication, cart, orders, admin functions)
↓
[ Database ]
(SQLite or MySQL – stores users, products, and orders)


---

## 🧪 Installation & Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/abe-echarry/grocery-delivery-system.git
   cd grocery-delivery-system

##Create a virtual environment:

python3 -m venv venv
source venv/bin/activate


##Install dependencies:

pip install -r requirements.txt


##Run database migrations:

python manage.py migrate


##Start the local server:

python manage.py runserver


##Open your browser and visit:

http://127.0.0.1:8000/

