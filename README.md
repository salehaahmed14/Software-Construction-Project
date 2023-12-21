# Software-Construction-Project
# Food-Delivery-Website-with-a-Dialog-Flow-based-ChatBot
Introducing FreshFoodEatery – a food delivery platform. The website features a user-friendly HTML/CSS frontend. With FastAPI backend, the system handles user interactions and order processing.
At the core of the platform lies a MySQL-based database consisting of three main tables orders, food_items and order_tracking alongwith stored procedures and functions to get and compute order prices.

In order to place new orders and track existing orders I've integrated Dialogflow's NLP chatbot technology. This chatbot has been trained to assist users in placing orders and offers order tracking updates. This interaction adds convenience and a personalized touch to the food delivery experience.

# Usage
## Prerequisites

Before you begin, ensure you have the following tools and software installed on your computer:

1. **Web Browser:** A modern web browser such as Chrome, Firefox, or Edge is required.

2. **Python:** This project utilizes the FastAPI backend, which necessitates the installation of Python. You can download and install Python from the official [Python website](https://www.python.org/downloads/).

3. **MySQL Database:** A MySQL database server is needed. You can obtain and install MySQL from the official [MySQL website](https://dev.mysql.com/downloads/).

4. **MySQL Client:** To interact with the database, you'll need a MySQL client. I recommend using [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) for its user-friendly interface.

## Setting Up the Project

1. **Clone the Repository:** Begin by cloning this repository to your local machine using Git or downloading the ZIP file.
2. 
2. **Backend Setup:**

- Navigate to the `backend` directory within the project folder:
  ```
  cd food-delivery-project/backend
  ```

- Create a virtual environment (optional but recommended):
  ```
  python -m venv venv
  On Windows: venv\Scripts\activate
  ```

- Install project dependencies:
  ```
  pip install mysql-connector-python
  pip install fastapi[all]
  ```

- Run the FastAPI backend:
  ```
  uvicorn main:app --reload
  ```

3. **Database Setup:**

- Update the database configuration in `backend/db_helper.py`.

- Open MySQL Workbench, create a connection, click on server, data import, check import from self contained file, copy the db schema path, click on import path and then start import.
- set it as default schema

4. **Frontend Setup:**

- Access the `frontend` directory.

- Open the `website.html` file in a web browser (using live server) to access the FoodEase website.

5. **Chatbot Integration:**

- The Dialogflow-based NLP chatbot is already integrated into the frontend. Ensure you have an active Dialogflow account and API key if you wish to customize or expand the chatbot's capabilities. Interact with the Chatbot here.
[https://bot.dialogflow.com/2ce45496-bfeb-4518-affd-2fdc5b334a2a](https://bot.dialogflow.com/d3867d0e-4dd0-4b4b-9f7f-dd3560f0a2ef)
- Using the DialogFlow folder, import the agent. 
## Usage
- Since fastAPI provides you with an http url, it is necessary to convert it into https, which can be done using ngrok, install ngrok in the folder, run your backend and then open the folder in your command prompt and run the command:
```
  ngrok http 8000
``` 
- This will provide you a new https url  that creates a secure tunnel to expose a local server to the internet. Paste it in the fulfillments-->URL section of your DialogFlow chatbot.
- You can now explore the FreshFood Eatery website, view menu and interact with the chatbot to place order and track orders.



