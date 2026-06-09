class SupplierService:
    """Service class to manage supplier operations."""

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def _connect_and_get_cursor(self):
        """Connect to DB and return the cursor."""
        self.db_connection.connect()
        return self.db_connection.get_cursor()


    def search_supplier(self):
        """Search and display a supplier by ID."""
        try:
            sid = input("Enter Supplier ID: ").strip()
            if not sid:
                print("Supplier ID cannot be empty.")
                return

            cursor = self._connect_and_get_cursor()
            cursor.execute("SELECT * FROM supplier WHERE supid = %s", (sid,))
            result = cursor.fetchall()

            if result:
                print("\n------ Supplier Details ------")
                for row in result:
                    self._print_supplier(row)
            else:
                print("No supplier found with the provided ID.")

        except Exception as e:
            print(f"Error occurred while searching supplier: {e}")

    def show_all_supplier_details(self):
        """Display all supplier records."""
        try:
            cursor = self._connect_and_get_cursor()
            cursor.execute("SELECT * FROM supplier")
            results = cursor.fetchall()

            if results:
                print("\n------ All Supplier Details ------")
                for row in results:
                    self._print_supplier(row)
            else:
                print("No supplier records found.")

        except Exception as e:
            print(f"Error occurred while retrieving suppliers: {e}")

    def update_supplier(self):
        """Update supplier details."""
        try:
            sid = input("Enter Supplier ID to update: ").strip()
            if not sid:
                print("Supplier ID cannot be empty.")
                return

            supname = input("Enter New Supplier Name: ").strip()
            sup_address = input("Enter New Address: ").strip()
            sup_nic = input("Enter New NIC: ").strip()
            sup_tel = input("Enter New Telephone: ").strip()
            sup_email = input("Enter New Email: ").strip()

            cursor = self._connect_and_get_cursor()
            sql = """
                UPDATE supplier
                SET supName = %s, supAddress = %s, supNic = %s, supTel = %s, supEmail = %s
                WHERE supid = %s
            """
            values = (supname, sup_address, sup_nic, sup_tel, sup_email, sid)
            cursor.execute(sql, values)
            self.db_connection.commit()

            if cursor.rowcount >= 1:
                print("Supplier record updated successfully.")
            else:
                print("No supplier found with the given ID.")

        except Exception as e:
            print(f"Error occurred while updating supplier: {e}")

    def delete_supplier(self):
        """Delete a supplier by ID."""
        try:
            sid = input("Enter Supplier ID to delete: ").strip()
            if not sid:
                print("Supplier ID cannot be empty.")
                return

            cursor = self._connect_and_get_cursor()
            cursor.execute("DELETE FROM supplier WHERE supid = %s", (sid,))
            self.db_connection.commit()

            if cursor.rowcount >= 1:
                print(f"{cursor.rowcount} supplier record(s) deleted successfully.")
            else:
                print("No supplier found with the provided ID.")

        except Exception as e:
            print(f"Error occurred while deleting supplier: {e}")

    def add_supplier(self):
        """Add a new supplier."""
        try:
            supname = input("Enter Supplier Name: ").strip()
            sup_address = input("Enter Address: ").strip()
            sup_nic = input("Enter NIC: ").strip()
            sup_tel = input("Enter Telephone: ").strip()
            sup_email = input("Enter Email: ").strip()

            if not all([supname, sup_address, sup_nic, sup_tel, sup_email]):
                print("All fields are required.")
                return

            cursor = self._connect_and_get_cursor()
            sql = """
                INSERT INTO supplier (supName, supAddress, supNic, supTel, supEmail)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (supname, sup_address, sup_nic, sup_tel, sup_email)
            cursor.execute(sql, values)
            self.db_connection.commit()

            print("New supplier record added successfully.")

        except Exception as e:
            print(f"Error occurred while adding supplier: {e}")

    def _print_supplier(self, row):
        """Helper method to format and print a supplier record."""
        print("---------------------------------")
        print(f"| Supplier ID     : {row[0]}")
        print(f"| Name            : {row[1]}")
        print(f"| Address         : {row[2]}")
        print(f"| NIC             : {row[3]}")
        print(f"| Telephone       : {row[4]}")
        print(f"| Email           : {row[5]}")
