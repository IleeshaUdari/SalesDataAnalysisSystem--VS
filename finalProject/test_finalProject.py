import pytest
from unittest.mock import patch, MagicMock
from DBConnection import DatabaseConnection, AuthenticationService
from BranchManager import BranchService
from ProductManager import ProductService
from BranchProductManger import BranchProductService
from SalesManager import SalesService
from SupplierManager import SupplierService
from StockManager import StockService
from ReportManager import ReportService
from finalproject import (
    main_menu,
    manage_products,
    manage_sales,
    manage_branch,
    manage_stock_details,
    manage_branch_product,
    manage_supplier_details,
    manage_reports
)

# Test for main_menu function
@patch('builtins.input', side_effect=['Admin', '111', '8'])
@patch('DBConnection.DatabaseConnection.connect')
@patch('DBConnection.DatabaseConnection.close')
@patch('DBConnection.AuthenticationService.authenticate', return_value=True)
def test_main_menu(mock_authenticate, mock_close, mock_connect, mock_input):
    db_connection = MagicMock(spec=DatabaseConnection)
    with patch('DBConnection.DatabaseConnection', return_value=db_connection):
        with patch('DBConnection.AuthenticationService', return_value=MagicMock(spec=AuthenticationService)):
            with patch('ProductManager.ProductService', return_value=MagicMock(spec=ProductService)):
                with patch('BranchManager.BranchService', return_value=MagicMock(spec=BranchService)):
                    with patch('BranchProductManger.BranchProductService', return_value=MagicMock(spec=BranchProductService)):
                        with patch('SupplierManager.SupplierService', return_value=MagicMock(spec=SupplierService)):
                            with patch('SalesManager.SalesService', return_value=MagicMock(spec=SalesService)):
                                with patch('StockManager.StockService', return_value=MagicMock(spec=StockService)):
                                    with patch('ReportManager.ReportService', return_value=MagicMock(spec=ReportService)):
                                        main_menu()
    mock_connect.assert_called_once()
    mock_authenticate.assert_called_once_with('Admin', '111')
    mock_close.assert_called_once()

# Test for manage_products function
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6', '7'])
def test_manage_products(mock_input):
    product_service = MagicMock(spec=ProductService)
    manage_products(product_service)
    product_service.add_product.assert_called_once()

# Test for manage_sales function
@patch('builtins.input', side_effect=['1', '2', '3', '4'])
def test_manage_sales(mock_input):
    sales_service = MagicMock(spec=SalesService)
    manage_sales(sales_service)
    sales_service.add_sales.assert_called_once()

# Test for manage_branch function
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_branch(mock_input):
    branch_service = MagicMock(spec=BranchService)
    manage_branch(branch_service)
    branch_service.add_branch.assert_called_once()

# Test for manage_stock_details function
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])
def test_manage_stock_details(mock_input):
    stock_service = MagicMock(spec=StockService)
    manage_stock_details(stock_service)
    stock_service.add_stock_details.assert_called_once()

# Test for manage_branch_product function
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_branch_product(mock_input):
    branch_product_service = MagicMock(spec=BranchProductService)
    manage_branch_product(branch_product_service)
    branch_product_service.add_branch_product.assert_called_once()

# Test for manage_supplier_details function
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_supplier_details(mock_input):
    supplier_service = MagicMock(spec=SupplierService)
    manage_supplier_details(supplier_service)
    supplier_service.add_supplier.assert_called_once()

# Test for manage_reports function
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_reports(mock_input):
    report_service = MagicMock(spec=ReportService)
    manage_reports(report_service)
    report_service.monthly_sales_analysis.assert_called_once()
