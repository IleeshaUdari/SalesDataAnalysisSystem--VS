class BranchProductService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def _execute_query(self, query, params=None, fetch=False):
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            self.db_connection.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def add_branch_product(self, bcode, proid, proqty):
        query = """
            INSERT INTO branchproduct (branchId, productId, branchqty)
            VALUES (%s, %s, %s)
        """
        result = self._execute_query(query, (bcode, proid, proqty))
        if result:
            print("New Branch Product record added successfully.")
        else:
            print("Failed to add Branch Product record.")

    def search_branch_product(self, bcode):
        query = "SELECT * FROM branchproduct WHERE branchId = %s"
        result = self._execute_query(query, (bcode,), fetch=True)
        if result:
            for x in result:
                print("----------------------------")
                print('| BranchProduct ID: ', x[0])
                print('| Branch ID: ', x[1])
                print('| Product ID: ', x[2])
                print('| Product Qty: ', x[3])
            print("--------------End Search Result--------------")
        else:
            print("No results found.")

    def search_branch_product_by_product_id(self, pid, bid):
        query = """
            SELECT * FROM branchproduct
            WHERE productId = %s AND branchId = %s
        """
        result = self._execute_query(query, (pid, bid), fetch=True)
        if result:
            return int(result[0][0])  
        return None

    def search_branch_product_for_stock(self, pid, bid):
        query = """
            SELECT * FROM branchproduct
            WHERE productId = %s AND branchId = %s
        """
        result = self._execute_query(query, (pid, bid), fetch=True)
        if result:
            bpid = result[0][0]
            pqty = result[0][3]
            return [bpid, pqty]
        return None

    def delete_branch_product(self, bcode, prid):
        query = """
            DELETE FROM branchproduct
            WHERE branchId = %s AND productId = %s
        """
        result = self._execute_query(query, (bcode, prid))
        if result:
            print("Branch Product record deleted successfully.")
        else:
            print("Record not found or failed to delete.")

    def update_branch_product(self, bcode, proid, proqty):
        query = """
            UPDATE branchproduct
            SET branchqty = %s
            WHERE branchId = %s AND productId = %s
        """
        result = self._execute_query(query, (proqty, bcode, proid))
        if result:
            print("Branch Product record updated successfully.")
        else:
            print("Failed to update record.")

    def update_branch_product_for_stock(self, bpid, proqty):
        query = """
            UPDATE branchproduct
            SET branchqty = %s
            WHERE bpid = %s
        """
        result = self._execute_query(query, (proqty, bpid))
        if result:
            print("Stock quantity updated.")
        else:
            print("Failed to update stock.")

    def show_all_branch_products(self):
        query = "SELECT * FROM branchproduct"
        result = self._execute_query(query, fetch=True)
        if result:
            for x in result:
                print("---------------------------------")
                print('Branch Product Code: ', x[0], '| Branch Code: ', x[1], '| Product Id: ', x[2], '| Product Qty: ', x[3])
            print("--------------End of List--------------")
        else:
            print("No branch product records found.")
