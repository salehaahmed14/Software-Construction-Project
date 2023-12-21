import mysql.connector
import unittest
from db_helper import (
    get_order_status,
    get_next_order_id,
    insert_order_item,
    get_total_order_price,
    insert_order_tracking,
    insert_customer_order
)

class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a testing database connection
        cls.cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", #enter your own password
            database="test_freshfood_eatery"
        )
        # Create tables and insert sample data for testing
        cls._create_test_tables()

    @classmethod
    def tearDownClass(cls):
        # Close the testing database connection
        cls.cnx.close()

    def setUp(self):
        # Additional setup before each test case if needed
        pass

    def tearDown(self):
        cursor = self.cnx.cursor()

        # Delete data from all tables
        cursor.execute("DELETE FROM `order_tracking`;")
        cursor.execute("DELETE FROM `orders`;")
        cursor.execute("DELETE FROM `customer_orders`;")
        cursor.execute("DELETE FROM `food_items`;")

        # Commit changes to the database
        self.cnx.commit()

    @classmethod
    def _create_test_tables(cls):
        cursor = cls.cnx.cursor()

        # Drop existing tables (if they exist)
        cursor.execute("DROP TABLE IF EXISTS `order_tracking`;")
        cursor.execute("DROP TABLE IF EXISTS `orders`;")
        cursor.execute("DROP TABLE IF EXISTS `customer_orders`;")
        cursor.execute("DROP TABLE IF EXISTS `food_items`;")

        # Create food_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `food_items` (
              `item_id` int NOT NULL,
              `name` varchar(255) DEFAULT NULL,
              `price` decimal(10,2) DEFAULT NULL,
              PRIMARY KEY (`item_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Insert sample data into food_items
        cursor.execute("""
            INSERT INTO `food_items` VALUES
            (1,'Pizza',6.00),(2,'Chicken Burger',7.00),
            (3,'Plain Fries',8.00),(4,'Beef Burger',5.00),
            (5,'Loaded Fries',6.00),(6,'Biryani',9.00),
            (7,'Chicken Curry',4.00),(8,'Pasta',7.00),
            (9,'Fried Chicken',5.00);
        """)

        # Create order_tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `order_tracking` (
              `order_id` int NOT NULL,
              `status` varchar(255) DEFAULT NULL,
              PRIMARY KEY (`order_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Insert sample data into order_tracking
        cursor.execute("""
            INSERT INTO `order_tracking` VALUES (40,'delivered'),(41,'in transit');
        """)

        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `orders` (
              `order_id` int NOT NULL,
              `item_id` int NOT NULL,
              `quantity` int DEFAULT NULL,
              `total_price` decimal(10,2) DEFAULT NULL,
              PRIMARY KEY (`order_id`,`item_id`),
              KEY `orders_ibfk_1` (`item_id`),
              CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `food_items` (`item_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Insert sample data into orders
        cursor.execute("""
            INSERT INTO `orders` VALUES
            (40,1,2,12.00),(40,3,1,8.00),
            (41,4,3,15.00),(41,6,2,18.00),(41,9,4,20.00);
        """)

        # Create customer_orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `customer_orders` (
              `order_id` INT AUTO_INCREMENT PRIMARY KEY,
              `name` VARCHAR(255) NOT NULL,
              `email` VARCHAR(255) NOT NULL,
              `phone` VARCHAR(20) NOT NULL,
              `address` TEXT NOT NULL,
              `payment_method` VARCHAR(20) NOT NULL,
              `order_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Commit changes to the database
        cls.cnx.commit()

    def test_get_order_status_existing_order(self):

        """
        test_get_order_status_existing_order:

        Objective: Verify that the correct status is returned for an existing order.
        Strategy: Check if the status returned matches the expected status for an existing order (e.g., "delivered").
        Assertion: self.assertEqual(result, expected_status)
        """

        # Test Case: Existing Order ID
        order_id = 40
        expected_status = "delivered"

        # Perform the test
        result = get_order_status(order_id)
        self.assertEqual(result, expected_status)
        print("Order exists.")

    def test_get_order_status_non_existing_order(self):

        """
        test_get_order_status_non_existing_order:

        Objective: Confirm that None is returned for a non-existing order.
        Strategy: Use an order_id that doesn't exist in the test data.
        Assertion: self.assertIsNone(result)
        """

        # Test Case: Non-Existing Order ID
        order_id = 100

        # Perform the test
        result = get_order_status(order_id)
        self.assertIsNone(result)
        print("Order doesnot exist.")
    
    def test_get_next_order_id(self):
        
        """
        test_get_next_order_id:

        Objective: Ensure that the next order_id is generated correctly.
        Strategy: Call the function and check if the result is greater than the highest existing order_id.
        Assertion: self.assertGreater(result, 41, ...)
        """

        # Call the function
        result = get_next_order_id()

        # Assert that the result is greater than 1 (since the table is not empty)
        self.assertGreater(result, 41, "For a non-empty orders table, the next order_id should be greater than 41.")

    def test_insert_order_item_successful(self):

        """
        test_insert_order_item_successful:

        Objective: Check if an order item is inserted successfully.
        Strategy: Insert an order item and verify the result.
        Assertion: self.assertEqual(result, 1, ...)
        """

        order_id = get_next_order_id()
        # Call the function
        result = insert_order_item("Pizza", 2, order_id)

        # Assert that the result is 1, indicating successful insertion
        self.assertEqual(result, 1, "Order item should be inserted successfully.")
    
    def test_insert_order_tracking_successful(self):

        """
        test_insert_order_tracking_successful:

        Objective: Confirm that order tracking information is inserted successfully.
        Strategy: Insert order tracking information and check for success.
        Assertion: (No specific assertion in the provided code, consider checking the database or adding one)
        """

        order_id = 55
        status = "delivered"
        insert_order_tracking(order_id, status)
        print("Sucessfully inserted.")


    def test_get_total_order_price_valid_order_id(self):

        """
        test_get_total_order_price_valid_order_id:

        Objective: Validate that the total order price is calculated correctly.
        Strategy: Use a known order_id and check if the calculated total price matches the expected value.
        Assertion: self.assertEqual(result, expected_total_price, ...)
        """

        # Test Case: Valid Order ID
        order_id = 41
        expected_total_price = 53.00

        # Perform the test
        result = get_total_order_price(order_id)
        self.assertEqual(result, expected_total_price)
        print("Expected total price is correct.")
    

    def test_insert_customer_order_valid_input(self):

        """
        test_insert_customer_order_valid_input:

        Objective: Ensure that customer order information is inserted successfully.
        Strategy: Insert customer order information and check for success.
        Assertion: (No specific assertion in the provided code, consider checking the database or adding one)
        
        """
        # Test Case: Valid Input
        name = "John Doe"
        email = "john.doe@example.com"
        phone = "123-456-7890"
        address = "123 Main St, City"
        payment_method = "Credit Card"

        # Perform the test
        insert_customer_order(name, email, phone, address, payment_method)
        print("Record inserted successfully.")


if __name__ == '__main__':
    unittest.main()