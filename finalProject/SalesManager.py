from datetime import datetime

class SalesService:
    def __init__(self, db_connection, branch_id: int, user_id: int):
        self.db_connection = db_connection
        self.branch_id = branch_id
        self.user_id = user_id

    def _connect_and_cursor(self):
        self.db_connection.connect()
        return self.db_connection.get_cursor()

    def add_sales_item(self, bill_id: str) -> float:
        try:
            pcode = input("Enter Product Code: ").strip()
            pqty = float(input("Enter Product Quantity: "))

            product_data = self.search_product_get_id_and_price(pcode)
            if not product_data:
                print("Product not found.")
                return 0.0

            pid, price = product_data
            total = price * pqty

            branch_product = self.search_branch_product_for_stock(pid, self.branch_id)
            if not branch_product:
                print("Product not available in branch.")
                return 0.0

            branch_product_id, old_qty = branch_product
            new_qty = old_qty - pqty
            if new_qty < 0:
                print("Insufficient stock.")
                return 0.0

            self.update_branch_product_for_stock(branch_product_id, new_qty)

            cursor = self._connect_and_cursor()
            sql = "INSERT INTO salesitem (billId, qty, price, total, branchproductid) VALUES (%s, %s, %s, %s, %s)"
            val = (bill_id, pqty, price, total, branch_product_id)
            cursor.execute(sql, val)
            self.db_connection.commit()
            print("New sales item record added successfully.")
            return total
        except Exception as e:
            print("Error while adding sales item:", str(e))
            return 0.0

    def search_product_get_id_and_price(self, pcode: str) -> list:
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("SELECT pid, pname, punit, price, discount, priceAfterDiscount, pcode FROM product WHERE pcode = %s", (pcode,))
            result = cursor.fetchone()
            if result:
                pid, pname, punit, price, discount, pad, code = result
                print(f"""
---------------------------------
| Product ID: {pid}
| Product Name: {pname}
| Unit: {punit}
| Price: {price}
| Discount: {discount}
| Price After Discount: {pad}
| Code: {code}
---------------------------------
""")
                return [pid, price]
        except Exception as e:
            print("Error during product lookup:", str(e))
        return []

    def update_branch_product_for_stock(self, bpid: int, proqty: float):
        try:
            cursor = self._connect_and_cursor()
            sql = "UPDATE branchproduct SET branchqty = %s WHERE bpid = %s"
            cursor.execute(sql, (proqty, bpid))
            self.db_connection.commit()
            print("Branch product stock updated.")
        except Exception as e:
            print("Error updating branch product stock:", str(e))

    def search_branch_product_for_stock(self, pid: int, bid: int) -> list:
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("SELECT bpid, productId, branchId, branchqty FROM branchproduct WHERE productId = %s AND branchId = %s", (pid, bid))
            result = cursor.fetchone()
            if result:
                bpid, _, _, branchqty = result
                return [bpid, float(branchqty)]
        except Exception as e:
            print("Error searching branch stock:", str(e))
        return []

    def add_sales(self):
        try:
            bill_code = input("Enter Bill Code: ").strip()
            discount = float(input("Enter Discount (0.0 - 1.0): "))
            payment_type = input("Enter Payment Type (Cash/Card): ").strip()
            product_count = int(input("Enter Number of Products: "))

            total = 0.0
            for _ in range(product_count):
                total += self.add_sales_item(bill_code)

            print(f"\nBill Total Before Discount: {total:.2f}")
            today = datetime.today().strftime("%Y-%m-%d")
            after_discount = total * (1 - discount)
            print(f"Total After Discount: {after_discount:.2f}")

            cursor = self._connect_and_cursor()
            sql = """
                INSERT INTO salesbill (billcode, billdate, billTotal, discount, totalAfterDiscount, paymentType, userId, branchid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (bill_code, today, total, discount, after_discount, payment_type, self.user_id, self.branch_id)
            cursor.execute(sql, val)
            self.db_connection.commit()
            print("Sales bill recorded successfully.")
        except Exception as e:
            print("Error during sales entry:", str(e))

    def search_sales_bill_item(self, billcode: str):
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("SELECT * FROM salesitem WHERE billId = %s", (billcode,))
            for count, item in enumerate(cursor.fetchall(), start=1):
                print(f"""
-- Bill Item ({count}) --------
| Branch Product Id: {item[5]}
| Qty: {item[2]}
| Price: {item[3]}
| Total: {item[4]}
-------------------------------
""")
        except Exception as e:
            print("Error retrieving sales bill items:", str(e))

    def search_sales_bill(self):
        try:
            billcode = input("Enter Bill Code: ").strip()
            cursor = self._connect_and_cursor()
            cursor.execute("SELECT * FROM salesbill WHERE billcode = %s", (billcode,))
            for x in cursor.fetchall():
                print(f"""
--------------------------------------
| Bill Code: {x[0]}
| Date: {x[1]}
| Total: {x[2]}
| Discount: {x[3]}
| Total After Discount: {x[4]}
| Payment Type: {x[5]}
| Branch ID: {x[6]}
| User ID: {x[7]}
--------------------------------------
""")
            self.search_sales_bill_item(billcode)
        except Exception as e:
            print("Error searching sales bill:", str(e))

    def show_all_bill_records_today(self):
        try:
            today = datetime.today().strftime("%Y-%m-%d")
            cursor = self._connect_and_cursor()
            cursor.execute("SELECT * FROM salesbill WHERE billdate = %s", (today,))
            for x in cursor.fetchall():
                print(f"""
--------------------------------------
| Bill Code: {x[0]}
| Date: {x[1]}
| Branch: {x[6]}
| User ID: {x[7]}
| Total: {x[2]}
| Discount: {x[3]}
| Total After Discount: {x[4]}
--------------------------------------
""")
        except Exception as e:
            print("Error retrieving today's sales:", str(e))

    def monthly_sales_analysis(self):
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("""
                SELECT branchid, YEAR(billdate), MONTH(billdate), SUM(billTotal)
                FROM salesbill
                GROUP BY branchid, YEAR(billdate), MONTH(billdate)
                ORDER BY branchid, YEAR(billdate), MONTH(billdate)
            """)
            for row in cursor.fetchall():
                print(f"""
---------------------------------
| Branch ID: {row[0]}
| Year: {row[1]}
| Month: {row[2]}
| Total Sales: {row[3]:.2f}
---------------------------------
""")
        except Exception as e:
            print("Error generating monthly sales report:", str(e))

    def weekly_sales_analysis(self):
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("""
                SELECT sb.branchid, b.branchName, YEAR(sb.billdate), WEEK(sb.billdate), SUM(sb.billTotal)
                FROM salesbill sb
                INNER JOIN branch b ON sb.branchid = b.brid
                GROUP BY sb.branchid, YEAR(sb.billdate), WEEK(sb.billdate)
                ORDER BY sb.branchid, YEAR(sb.billdate), WEEK(sb.billdate)
            """)
            for row in cursor.fetchall():
                print(f"""
---------------------------------
| Branch ID: {row[0]}
| Branch Name: {row[1]}
| Year: {row[2]}
| Week: {row[3]}
| Total Sales: {row[4]:.2f}
---------------------------------
""")
        except Exception as e:
            print("Error generating weekly sales report:", str(e))

    def sales_product_preferences(self):
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("""
                SELECT si.branchproductid, SUM(si.qty), COUNT(DISTINCT si.billId), SUM(si.total)
                FROM salesitem si
                JOIN salesbill sb ON si.billId = sb.billcode
                GROUP BY si.branchproductid
                ORDER BY SUM(si.qty) DESC
            """)
            for row in cursor.fetchall():
                print(f"""
---------------------------------
| Branch Product ID: {row[0]}
| Total Quantity Sold: {row[1]}
| No. of Sales: {row[2]}
| Total Revenue: {row[3]:.2f}
---------------------------------
""")
        except Exception as e:
            print("Error generating product preference report:", str(e))

    def final_sales_analysis(self):
        try:
            cursor = self._connect_and_cursor()
            cursor.execute("""
                SELECT branchid,
                       COUNT(billcode),
                       SUM(total_sales),
                       AVG(total_sales),
                       MIN(total_sales),
                       MAX(total_sales)
                FROM (
                    SELECT billcode, branchid, SUM(billTotal) AS total_sales
                    FROM salesbill
                    GROUP BY billcode, branchid
                ) AS sub
                GROUP BY branchid
                ORDER BY branchid
            """)
            for row in cursor.fetchall():
                print(f"""
---------------------------------
| Branch ID: {row[0]}
| No. of Sales: {row[1]}
| Total Sales Amount: {row[2]:.2f}
| Average Sale: {row[3]:.2f}
| Minimum Sale: {row[4]:.2f}
| Maximum Sale: {row[5]:.2f}
---------------------------------
""")
        except Exception as e:
            print("Error generating final sales analysis:", str(e))
