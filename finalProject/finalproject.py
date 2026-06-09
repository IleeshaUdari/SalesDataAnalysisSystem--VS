import os
import platform
import subprocess
import pandas as pd  

from DBConnection import DatabaseConnection, AuthenticationService
from BranchManager import BranchService
from ProductManager import ProductService
from BranchProductManger import BranchProductService
from SalesManager import SalesService
from SupplierManager import SupplierService
from StockManager import StockService
from ReportManager import ReportService

def open_excel_file (sampathexcel):
    if platform.system() == 'Windows':
        os.startfile(sampathexcel)  
    elif platform.system() == 'Darwin':  
        subprocess.call(['open', sampathexcel])
    else:  
        subprocess.call(['xdg-open', sampathexcel])

def view_excel_file(sampathexcel):
    if os.path.exists(sampathexcel):
        try:
            df = pd.read_excel(sampathexcel)  
            print("\n--- Excel File Preview ---")
            print(df.head(20)) 
            print("-------------------------\n")
            open_choice = input("Do you want to open the full Excel file? (y/n): ").strip().lower()
            if open_choice == 'y':
                open_excel_file(sampathexcel)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
    else:
        print("Done!", sampathexcel)


def main_menu():
    
    db_connection = DatabaseConnection()
    db_connection.connect()

    auth_service = AuthenticationService(db_connection)
    product_service = ProductService(db_connection)
    branch_service = BranchService(db_connection)
    branch_product_service = BranchProductService(db_connection)
    supplier_service = SupplierService(db_connection)
    report_service = ReportService(db_connection)

    print("\n------------WELCOME TO SAMPATH FOOD CITY (PVT) LTD---------------")
    username = input("Enter username: ")
    password = input("Enter password: ")

    mybranch_id = 1

    user = auth_service.authenticate(username, password)

    sales_service = SalesService(db_connection, mybranch_id, user)
    stock_service = StockService(db_connection, mybranch_id, user)

    if user:
        print("\nLogged in successfully...\n")
       
        while True:
            print("===========================================")
            print("               Main Menu                   ")
            print("===========================================")
            print("|  1 - Manage Product Details             |")
            print("|  2 - Manage Sales Details               |")
            print("|  3 - Manage Branch Details              |")
            print("|  4 - Manage Stock Details               |")
            print("|  5 - Manage Branch Product Details      |")
            print("|  6 - Manage Supplier Details            |")
            print("|  7 - Reports                            |")
            print("|  8 - Exit                               |")
            print("===========================================")
            choice = input("Enter your choice: ")

            if choice == "1":
                manage_products(product_service)
            elif choice == "2":
                manage_sales(sales_service)
            elif choice == "3":
                manage_branch(branch_service)
            elif choice == "4":
                manage_stock_details(stock_service)
            elif choice == "5":
                manage_branch_product(branch_product_service)
            elif choice == "6":
                manage_supplier_details(supplier_service)
            elif choice == "7":
                manage_reports(report_service)
            elif choice == "8":
                print("\nExiting application... Goodbye!")
                break
            else:
                print("\nInvalid choice, please try again.\n")
    else:
        print("\nInvalid username or password. Access denied.\n")

    db_connection.close()


def manage_products(product_service):
    while True:
        print("\n--------- Manage Product Details --------")
        print("|  1 - Add Product Details                |")
        print("|  2 - Search Product Details             |")
        print("|  3 - Delete Product Details             |")
        print("|  4 - Update Product Details             |")
        print("|  5 - Update Product Price Level         |")
        print("|  6 - Search All Products (View Excel)   |")
        print("|  7 - Exit (Back to Main Menu)           |")
        print("-------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Add Product Details --")
            product_service.add_product()
        elif choice == "2":
            print("\n-- Search Product Details --")
            product_service.search_product()
          
            view_excel = input("Do you want to view the full product Excel file? (y/n): ").lower()
            if view_excel == 'y':
                view_excel_file('data/products.xlsx')
        elif choice == "3":
            print("\n-- Delete Product Details --")
            product_service.delete_product()
        elif choice == "4":
            print("\n-- Update Product Details --")
            product_service.update_product()
        elif choice == "5":
            print("\n-- Update Product Price Level --")
            product_service.update_product_price_level()
        elif choice == "6":
            print("\n-- Show All Products (Excel View) --")
            product_service.show_all_products()
            view_excel_file('data/products.xlsx')
        elif choice == "7":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


def manage_branch(branch_service):
    while True:
        print("\n--------- Manage Branch Details ---------")
        print("|  1 - Add Branch Details                 |")
        print("|  2 - Search Branch Details              |")
        print("|  3 - Delete Branch Details              |")
        print("|  4 - Update Branch Details              |")
        print("|  5 - Search All Branches (View Excel)   |")
        print("|  6 - Exit (Back to Main Menu)           |")
        print("-------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Add Branch Details --")
            branch_service.add_branch()
        elif choice == "2":
            print("\n-- Search Branch Details --")
            branch_service.search_branch()
            view_excel = input("Do you want to view the full branch Excel file? (y/n): ").lower()
            if view_excel == 'y':
                view_excel_file('data/branches.xlsx')
        elif choice == "3":
            print("\n-- Delete Branch Details --")
            branch_service.delete_branch()
        elif choice == "4":
            print("\n-- Update Branch Details --")
            branch_service.update_branch()
        elif choice == "5":
            print("\n-- Show All Branches (Excel View) --")
            branch_service.show_all_branches()
            view_excel_file('data/branches.xlsx')
        elif choice == "6":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


def manage_branch_product(branch_product_service):
    while True:
        print("\n--------- Manage Branchwise Product Details --------")
        print("|  1 - Add Branch Product Details                    |")
        print("|  2 - Search Branch Product Details                 |")
        print("|  3 - Delete Branch Product Details                 |")
        print("|  4 - Update Branch Product Details                 |")
        print("|  5 - Search All Branch Products (View Excel)       |")
        print("|  6 - Exit (Back to Main Menu)                      |")
        print("------------------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Add Branch Product Details --")
            branch_product_service.add_branch_product()
        elif choice == "2":
            print("\n-- Search Branch Product Details --")
            branch_product_service.search_branch_product()
            view_excel = input("Do you want to view the full branch product Excel file? (y/n): ").lower()
            if view_excel == 'y':
                view_excel_file('data/branch_products.xlsx')
        elif choice == "3":
            print("\n-- Delete Branch Product Details --")
            branch_product_service.delete_branch_product()
        elif choice == "4":
            print("\n-- Update Branch Product Details --")
            branch_product_service.update_branch_product()
        elif choice == "5":
            print("\n-- Show All Branch Products (Excel View) --")
            branch_product_service.show_all_branch_products()
            view_excel_file('data/branch_products.xlsx')
        elif choice == "6":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


def manage_sales(sales_service):
    while True:
        print("\n----------- Manage Sales Details ------------")
        print("|  1 - Add Sales Details                      |")
        print("|  2 - Show Sales Bill Details (Search)       |")
        print("|  3 - Show All Sales Bill Details (Today)    |")
        print("|  4 - Exit (Back to Main Menu)               |")
        print("-----------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Add Sales Details --")
            sales_service.add_sales()
        elif choice == "2":
            print("\n-- Search Sales Bill Details --")
            sales_service.search_sales_bill()
            view_excel = input("Do you want to view the full sales bill Excel file? (y/n): ").lower()
            if view_excel == 'y':
                view_excel_file('data/sales_bills.xlsx')
        elif choice == "3":
            print("\n-- Show All Sales Bill Details (Today) --")
            sales_service.show_all_sales_today()
            view_excel_file('data/sales_bills.xlsx')
        elif choice == "4":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


def manage_stock_details(stock_service):
    while True:
        print("\n------------ Manage Stock Details --------------")
        print("|  1 - Add Stock Details                         |")
        print("|  2 - Search Stock Details                      |")
        print("|  3 - Show All Stock Details                    |")
        print("|  4 - Exit (Back to Main Menu)                  |")
        print("--------------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Add Stock Details --")
            stock_service.add_stock()
        elif choice == "2":
            print("\n-- Search Stock Details --")
            stock_service.search_stock()
            view_excel = input("Do you want to view the full stock Excel file? (y/n): ").lower()
            if view_excel == 'y':
                view_excel_file('data/stock.xlsx')
        elif choice == "3":
            print("\n-- Show All Stock Details --")
            stock_service.show_all_stock()
            view_excel_file('data/stock.xlsx')
        elif choice == "4":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


def manage_supplier_details(supplier_service):
    while True:
        print("\n----------- Manage Supplier Details ----------")
        print("|  1 - Add Supplier Details                    |")
        print("|  2 - Search Supplier Details                 |")
        print("|  3 - Show All Supplier Details               |")
        print("|  4 - Exit (Back to Main Menu)                |")
        print("------------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Add Supplier Details --")
            supplier_service.add_supplier()
        elif choice == "2":
            print("\n-- Search Supplier Details --")
            supplier_service.search_supplier()
            view_excel = input("Do you want to view the full supplier Excel file? (y/n): ").lower()
            if view_excel == 'y':
                view_excel_file('data/suppliers.xlsx')
        elif choice == "3":
            print("\n-- Show All Supplier Details --")
            supplier_service.show_all_suppliers()
            view_excel_file('data/suppliers.xlsx')
        elif choice == "4":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


def manage_reports(report_service):
    while True:
        print("\n--------------- Reports Menu ----------------")
        print("|  1 - Show Branch Product Report             |")
        print("|  2 - Show Sales Report                      |")
        print("|  3 - Exit (Back to Main Menu)               |")
        print("-----------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n-- Branch Product Report --")
            report_service.branch_product_report()
        elif choice == "2":
            print("\n-- Sales Report --")
            report_service.sales_report()
        elif choice == "3":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\nInvalid choice. Please select a valid option.")


if __name__ == "__main__":
    main_menu()
