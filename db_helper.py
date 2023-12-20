import mysql.connector
global cnx
cnx = mysql.connector.connect(
    host= "localhost",
    user="root",
    password="",
    database="FreshFood_eatery"
)

def get_order_status(order_id):
    
    """
    Fetches the order status from the order_tracking table.

    Parameters:
        - order_id (int): The ID of the order.

    Returns:
        - str: The order status.
    """

    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = ("SELECT status FROM order_tracking WHERE order_id= %s")

    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result is not None:
        return result[0]
    else:
        return None

def get_next_order_id():
   
    """
    Gets the next available order_id.

    Returns:
        - int: The next available order_id.
    """

    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

def insert_order_item(food_item, quantity, order_id):

    """
    Inserts an order item into the database.

    Parameters:
        - food_item (str): The name of the food item.
        - quantity (int): The quantity of the food item.
        - order_id (int): The ID of the order.

    Returns:
        - int: 1 if successful, -1 otherwise.
    """
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

def get_total_order_price(order_id):

    """
    Gets the total price of the order.

    Parameters:
        - order_id (int): The ID of the order.

    Returns:
        - float: The total price of the order.
    """
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result


def insert_order_tracking(order_id, status):

    """
    Inserts a record into the order_tracking table.

    Parameters:
        - order_id (int): The ID of the order.
        - status (str): The status of the order.

    Returns:
        - None
    """
    
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()

def insert_customer_order(name, email, phone, address, payment_method):

    """
    Inserts customer order information into the customer_orders table.

    Parameters:
        - name (str): Customer name.
        - email (str): Customer email.
        - phone (str): Customer phone number.
        - address (str): Customer address.
        - payment_method (str): Payment method.

    Returns:
        - None
    """

    try:
            cursor = cnx.cursor()

            # Insert the form data into the customer_orders table
            insert_query = """
                INSERT INTO customer_orders (name, email, phone, address, payment_method)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (name, email, phone, address, payment_method)
            cursor.execute(insert_query, values)

            # Commit the changes to the database
            cnx.commit()

            print("Form data inserted into customer_orders table.")

    except mysql.connector.Error as err:
        print(f"Error inserting customer order into the database: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        raise

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        raise