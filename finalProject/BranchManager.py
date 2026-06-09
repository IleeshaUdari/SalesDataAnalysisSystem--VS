class BranchService:
    """
    Service class responsible for managing branch-related operations.
    """

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def _execute_query(self, query, params=None, fetch=False):
        """
        Internal helper method to execute a database query safely.
        """
        try:
            self.db_connection.connect()
            cursor = self.db_connection.get_cursor()
            cursor.execute(query, params)

            if fetch:
                results = cursor.fetchall()
                self.db_connection.close()
                return results
            else:
                self.db_connection.commit()
                affected_rows = cursor.rowcount
                self.db_connection.close()
                return affected_rows
        except Exception as e:
            print(f"[ERROR] Database operation failed: {e}")
            self.db_connection.close()
            return None

    def add_branch(self, bcode, bname, badd, bmanager, bemp):
        """
        Adds a new branch record to the database.
        """
        sql = "INSERT INTO branch (brid, branchName, address, branchManager, totalEmployees) VALUES (%s, %s, %s, %s, %s)"
        val = (bcode, bname, badd, bmanager, bemp)
        result = self._execute_query(sql, val)
        if result:
            print("New Branch record added successfully.")
        else:
            print("Failed to add branch.")

    def delete_branch(self, bcode):
        """
        Deletes a branch record from the database using the branch code.
        """
        sql = "DELETE FROM branch WHERE brid=%s"
        result = self._execute_query(sql, (bcode,))
        if result and result > 0:
            print(f"{result} Branch record(s) deleted successfully.")
        else:
            print("No matching branch found or deletion failed.")

    def update_branch(self, bcode, bname, badd, bmanager, bemp):
        """
        Updates the details of an existing branch.
        """
        sql = "UPDATE branch SET branchName=%s, address=%s, branchManager=%s, totalEmployees=%s WHERE brid=%s"
        val = (bname, badd, bmanager, bemp, bcode)
        result = self._execute_query(sql, val)
        if result:
            print("Branch record updated successfully.")
        else:
            print("Update failed. Please check the branch code.")

    def search_branch(self, bcode):
        """
        Searches and displays details for a single branch using its code.
        """
        sql = "SELECT * FROM branch WHERE brid=%s"
        results = self._execute_query(sql, (bcode,), fetch=True)
        if results:
            for x in results:
                print("---------------------------------")
                print('| Branch ID: ', x[0])
                print('| Branch Name: ', x[1])
                print('| Branch Address: ', x[2])
                print('| Branch Manager: ', x[3])
                print('| Total Employees: ', x[4])
                print("---------------------------------")
        else:
            print("No branch found with the given ID.")

    def show_all_branches(self):
        """
        Displays all branch records in the database.
        """
        sql = "SELECT * FROM branch"
        results = self._execute_query(sql, fetch=True)
        if results:
            for x in results:
                print("---------------------------------")
                print('Branch Code: ', x[0], '| Branch Name: ', x[1], '| Address: ', x[2], '| Manager: ', x[3], '| Employees: ', x[4])
            print("--------------End Search Result--------------")
        else:
            print("No branch records found.")
