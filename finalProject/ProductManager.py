from datetime import datetime

class ProductService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def _fetch_product_by_code(self, pcode):
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        return cursor.fetchall()

    def _print_product_info(self, product):
        print("---------------------------------")
        print('| Product ID: ', product[0])
        print('| Product Name: ', product[1])
        print('| Product Unit: ', product[2])
        print('| Product Price: ', product[3])
        print('| Product Discount: ', product[4])
        print('| Product Price After Discount: ', product[5])
        print('| Product Code: ', product[6])
        print("---------------------------------")

    def search_product(self):
        pcode = input("Enter Product Code: ")
        products = self._fetch_product_by_code(pcode)
        if not products:
            print("No product found with the provided code.")
            return
        for product in products:
            self._print_product_info(product)
        print("--------------End Search Result--------------")

    def search_product_get_id_and_price(self, pcode) -> list:
        products = self._fetch_product_by_code(pcode)
        if not products:
            print("Product not found.")
            return []
        self._print_product_info(products[0])
        return [products[0][0], products[0][3]]

    def show_all_products(self):
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM product")
        results = cursor.fetchall()

        if not results:
            print("No products found.")
            return

        for product in results:
            print("---------------------------------")
            print('| Product Code: ', product[6])
            print('| ID: ', product[0])
            print('| Name: ', product[1])
            print('| Unit: ', product[2])
            print('| Price: ', product[3])
            print('| Discount: ', product[4])
            print('| Price After Discount: ', product[5])
            print("---------------------------------")
        print("--------------End Search Result--------------")

    def update_product(self):
        pcode = input("Enter Product Code: ")
        pname = input("Enter Product Name: ")
        unit = input("Enter Product unit: ")
        try:
            price = float(input("Enter Product Price: "))
            discount = float(input("Enter Product Discount: "))
        except ValueError:
            print("Invalid input for price or discount.")
            return
        price_after_discount = price - (discount * price)

        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        sql = """UPDATE product SET pname=%s, unit=%s, price=%s, 
                 discount=%s, priceAfterDiscount=%s WHERE pcode=%s"""
        val = (pname, unit, price, discount, price_after_discount, pcode)
        cursor.execute(sql, val)
        self.db_connection.commit()

        if cursor.rowcount >= 1:
            print("Product record updated successfully.")
        else:
            print("Product update failed. Check if product code exists.")

    def add_product_price_level(self, pcode, price):
        today_date = datetime.today().strftime("%Y-%m-%d")
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        sql = "INSERT INTO price (productId, price, startDate) VALUES (%s, %s, %s)"
        cursor.execute(sql, (pcode, price, today_date))
        self.db_connection.commit()
        print("Product price level record added successfully.")

    def update_product_price_level(self):
        pcode = input("Enter Product Code: ")
        try:
            price = float(input("Enter Product Price: "))
        except ValueError:
            print("Invalid input for price.")
            return

        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        sql = "UPDATE product SET price=%s WHERE pcode=%s"
        cursor.execute(sql, (price, pcode))
        self.db_connection.commit()

        if cursor.rowcount >= 1:
            print("Product price level updated successfully.")
            self.add_product_price_level(pcode, price)
        else:
            print("Update failed. Product not found.")

    def price_analysis(self):
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        cursor.execute("""
            SELECT p.pname, pr.productId, pr.startDate, pr.price, 
                   LAG(pr.price) OVER (PARTITION BY pr.productId ORDER BY pr.startDate) AS previous_price, 
                   (pr.price - LAG(pr.price) OVER (PARTITION BY pr.productId ORDER BY pr.startDate)) AS price_change 
            FROM price pr
            INNER JOIN product p ON pr.productId = p.pcode
        """)
        results = cursor.fetchall()

        if not results:
            print("No price history found.")
            return

        for row in results:
            print("---------------------------------|")
            print('| Product Code: ', row[1])
            print('| Product Name: ', row[0])
            print('| Start Date: ', row[2])
            print('| Price: ', row[3])
            print('| Previous Price: ', row[4])
            print("|--------------------------------|")
            print('| Price Change: ', row[5])
            print("|--------------------------------|")
        print("--------------End Report--------------")

    def delete_product(self):
        pcode = input("Enter Product Code: ")
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        sql = "DELETE FROM product WHERE pcode=%s"
        cursor.execute(sql, (pcode,))
        self.db_connection.commit()
        if cursor.rowcount >= 1:
            print(f"{cursor.rowcount} Product record deleted successfully.")
        else:
            print("Product not found. No deletion occurred.")

    def add_branch_product_for_new_product(self, bcode, proid):
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        sql = "INSERT INTO branchproduct (branchId, productId, branchqty) VALUES (%s, %s, %s)"
        cursor.execute(sql, (bcode, proid, "0"))
        self.db_connection.commit()
        print(f"Branch product added for Branch {bcode} and Product {proid}.")

    def all_branch_product_for_new_product(self, pcode):
        pdata = self.search_product_get_id_and_price(pcode)
        if not pdata:
            print("Product not found. Branch product records not added.")
            return
        proid = pdata[0]
        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branch")
        branches = cursor.fetchall()

        for branch in branches:
            print("---------------------------------")
            print('Branch Code: ', branch[0], '| Branch Name: ', branch[1])
            self.add_branch_product_for_new_product(branch[0], proid)

    def add_product(self):
        pcode = input("Enter Product Code: ")
        pname = input("Enter Product Name: ")
        unit = input("Enter Product Unit: ")
        try:
            price = float(input("Enter Product Price: "))
            discount = float(input("Enter Product Discount: "))
        except ValueError:
            print("Invalid input for price or discount.")
            return
        price_after_discount = price - (discount * price)

        self.db_connection.connect()
        cursor = self.db_connection.get_cursor()
        sql = """INSERT INTO product 
                 (pname, unit, price, discount, priceAfterDiscount, pcode) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        val = (pname, unit, price, discount, price_after_discount, pcode)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("New product record added successfully.")

        self.add_product_price_level(pcode, price)
        self.all_branch_product_for_new_product(pcode)
