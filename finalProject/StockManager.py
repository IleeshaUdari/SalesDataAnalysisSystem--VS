from datetime import datetime

class StockService:
    def __init__(self, db_connection, branch_id, user_id):
        self.db_connection = db_connection
        self.branch_id = branch_id
        self.user_id = user_id[0][0] if isinstance(user_id, list) else user_id

    def search_product_get_id_and_price(self, pcode) -> list:
        cursor = self.db_connection.get_cursor()
        query = "SELECT * FROM product WHERE pcode=%s"
        cursor.execute(query, (pcode,))
        result = cursor.fetchone()
        if result:
            print("---------------------------------")
            print('| Product ID: ', result[0])
            print('| Product Name: ', result[1])
            print('| Product Unit: ', result[2])
            print('| Product Price: ', result[3])
            print('| Product Discount: ', result[4])
            print('| Product Price After Discount: ', result[5])
            print('| Product Code: ', result[6])
            print("---------------------------------")
            return [result[0], result[3]]
        else:
            print("Product not found.")
            return []

    def search_branch_product_for_stock(self, pid, bid) -> list:
        cursor = self.db_connection.get_cursor()
        query = "SELECT * FROM branchproduct WHERE productId=%s AND branchId=%s"
        cursor.execute(query, (pid, bid))
        result = cursor.fetchone()
        if result:
            return [result[0], result[3]]
        else:
            print("Branch product not found.")
            return []

    def update_branch_product_for_stock(self, bpid, proqty):
        cursor = self.db_connection.get_cursor()
        query = "UPDATE branchproduct SET branchqty=%s WHERE bpid=%s"
        cursor.execute(query, (proqty, bpid))
        self.db_connection.commit()
        print("Branch Product record updated successfully.")

    def add_stock_item(self, grn_id) -> float:
        try:
            pcode = input("Enter Product Code: ").strip()
            pqty = float(input("Enter Stock Qty: "))
            pprice = float(input("Enter Stock Price: "))
            ex_date = input("Enter Expire Date (YYYY-MM-DD): ").strip()
            mf_date = input("Enter MF Date (YYYY-MM-DD): ").strip()

            pdata = self.search_product_get_id_and_price(pcode)
            if not pdata:
                return 0.0

            pid = pdata[0]
            ptotal = pprice * pqty

            bdata = self.search_branch_product_for_stock(pid, self.branch_id)
            if not bdata:
                return 0.0

            pb_id = bdata[0]
            pb_qty_old = bdata[1]
            pb_qty_new = float(pb_qty_old) + pqty
            self.update_branch_product_for_stock(pb_id, pb_qty_new)

            cursor = self.db_connection.get_cursor()
            query = """INSERT INTO stockitem (qty, stockPrice, expDate, mfDate, grnBillNo, branchproductid)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (pqty, pprice, ex_date, mf_date, grn_id, pb_id))
            self.db_connection.commit()
            print("New Stock Item record added successfully.")
            return ptotal
        except Exception as e:
            print("Error adding stock item:", e)
            return 0.0

    def search_stock_grn_item_details(self, billcode):
        cursor = self.db_connection.get_cursor()
        query = "SELECT * FROM stockitem WHERE grnBillNo=%s"
        cursor.execute(query, (billcode,))
        results = cursor.fetchall()
        for idx, item in enumerate(results, 1):
            total = float(item[2]) * float(item[1])
            print(f"--GRN Item({idx})--------") 
            print('|      Branch Product Id: ', item[6])
            print('|      Qty   : ', item[1])
            print('|      Price : ', item[2])
            print('|      Total : ', total)
            print('|      EXP Date: ', item[3])
            print('|      MF Date: ', item[4])
            print("------------------------------------")

    def search_stock_grn_details(self):
        billcode = input("Enter GRN Bill Code: ").strip()
        cursor = self.db_connection.get_cursor()
        query = "SELECT * FROM grn WHERE grnBillNo=%s"
        cursor.execute(query, (billcode,))
        results = cursor.fetchall()
        for x in results:
            print("--------------------------------------|")
            print('| GRN Bill No: ', x[1])
            print('| Date: ', x[3])
            print('| Status: ', x[7])
            print('| Supplier ID: ', x[8])
            print('| Total                     : ', x[2])
            print('| Discount                  : ', x[4])
            print("|-------------------------------------|")
            print('| Bill Total(After Discount): ', x[5])
            print('| Paid Amount               : ', x[6])
            print("--------------------------------------|")
        self.search_stock_grn_item_details(billcode)
        print("--------------End Search Result--------------")

    def add_stock_details(self):
        try:
            grncode = input("Enter GRN Code: ").strip()
            supid = input("Enter Supplier Id: ").strip()
            stock_dis = float(input("Enter Discount (e.g. 0.05): "))
            paid_amount = float(input("Enter Paid Amount: "))
            pcount = int(input("Enter Product Type Count: "))

            grn_total = 0.0
            for _ in range(pcount):
                grn_total += self.add_stock_item(grncode)

            bill_date = datetime.today().strftime("%Y-%m-%d")
            total_after_discount = grn_total - (stock_dis * grn_total)
            status = "Payment Complete" if total_after_discount == paid_amount else "Payment Not Complete"

            cursor = self.db_connection.get_cursor()
            query = """INSERT INTO grn 
                       (grnBillNo, total, date, discount, totalAfterDiscount, paidAmount, status, supplierId)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (grncode, grn_total, bill_date, stock_dis, total_after_discount, paid_amount, status, supid))
            self.db_connection.commit()
            print("New GRN Bill record added successfully.")
        except Exception as e:
            print("Error adding GRN details:", e)

    def show_all_stock_grn_records_today(self):
        bill_date = datetime.today().strftime("%Y-%m-%d")
        cursor = self.db_connection.get_cursor()
        query = "SELECT * FROM grn WHERE date=%s"
        cursor.execute(query, (bill_date,))
        results = cursor.fetchall()
        for x in results:
            print("--------------------------------------") 
            print('| GRN Bill No: ', x[1])
            print('| Date: ', x[3])
            print('| Status: ', x[7])
            print('| Supplier Id: ', x[8])
            print('| Total:                 ', x[2])
            print('| Discount:              ', x[4])
            print('| ------------------------------------') 
            print('| Total(After Discount): ', x[5])
            print('| Paid Amount:           ', x[6])
            print("--------------------------------------")   
        print("-----------End Search Result-------------")

    def search_stock_grn_payment_details(self, billcode) -> list:
        cursor = self.db_connection.get_cursor()
        query = "SELECT * FROM grn WHERE grnBillNo=%s"
        cursor.execute(query, (billcode,))
        result = cursor.fetchone()
        if result:
            return [result[6], result[5]]
        else:
            print("No such GRN record found.")
            return []

    def update_stock_grn_payment(self):
        try:
            grncode = input("Enter GRN Code: ").strip()
            pamount = float(input("Enter Newly Paid Amount: "))
            pdata = self.search_stock_grn_payment_details(grncode)
            if not pdata:
                return

            pamount_old, bill_amount = pdata
            total_paid = float(pamount_old) + pamount
            status = "Payment Complete" if total_paid == bill_amount else "Payment Not Complete"

            cursor = self.db_connection.get_cursor()
            query = "UPDATE grn SET paidAmount=%s, status=%s WHERE grnBillNo=%s"
            cursor.execute(query, (total_paid, status, grncode))
            self.db_connection.commit()
            print("GRN Payment record updated successfully.")
        except Exception as e:
            print("Error updating GRN payment:", e)
