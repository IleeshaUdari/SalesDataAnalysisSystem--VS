import pytest
from unittest.mock import patch, MagicMock
from ProductManager import ProductService

# Fixtures for shared mock objects
@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def product_service(mock_db):
    return ProductService(mock_db)

# Test for adding a product
@patch('builtins.input', side_effect=['101', 'Milk', '450'])
def test_add_product(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = None
    mock_db.cursor().lastrowid = 101

    product_service.add_product()

    mock_db.cursor().execute.assert_called()
    mock_db.commit.assert_called_once()

# Test for updating an existing product
@patch('builtins.input', side_effect=['101', 'Cheese', '550'])
def test_update_product(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = (101, 'Milk', 450)

    product_service.update_product()

    mock_db.cursor().execute.assert_called()
    mock_db.commit.assert_called_once()

# Test for deleting an existing product
@patch('builtins.input', side_effect=['101'])
def test_delete_product(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = (101, 'Cheese', 550)

    product_service.delete_product()

    mock_db.cursor().execute.assert_called()
    mock_db.commit.assert_called_once()

# Test for displaying all products
def test_display_all_products(product_service, mock_db):
    mock_db.cursor().fetchall.return_value = [
        (101, 'Milk', 450),
        (102, 'Cheese', 500)
    ]

    product_service.display_all_products()

    mock_db.cursor().execute.assert_called_once()

# Test for searching a product by ID
@patch('builtins.input', side_effect=['101'])
def test_search_product_by_id(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = (101, 'Butter', 600)

    product_service.search_product_by_id()

    mock_db.cursor().execute.assert_called_once()

# Test for searching a product by name
@patch('builtins.input', side_effect=['Milk'])
def test_search_product_by_name(mock_input, product_service, mock_db):
    mock_db.cursor().fetchall.return_value = [(101, 'Milk', 450)]

    product_service.search_product_by_name()

    mock_db.cursor().execute.assert_called_once()

# Edge Case: Adding product that already exists
@patch('builtins.input', side_effect=['101', 'Milk', '450'])
def test_add_product_existing(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = (101, 'Milk', 450)

    product_service.add_product()

    mock_db.cursor().execute.assert_not_called()
    mock_db.commit.assert_not_called()

# Edge Case: Updating non-existent product
@patch('builtins.input', side_effect=['999', 'Cream', '400'])
def test_update_product_nonexistent(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = None

    product_service.update_product()

    mock_db.cursor().execute.assert_not_called()
    mock_db.commit.assert_not_called()

# Edge Case: Deleting non-existent product
@patch('builtins.input', side_effect=['999'])
def test_delete_product_nonexistent(mock_input, product_service, mock_db):
    mock_db.cursor().fetchone.return_value = None

    product_service.delete_product()

    mock_db.cursor().execute.assert_not_called()
    mock_db.commit.assert_not_called()
