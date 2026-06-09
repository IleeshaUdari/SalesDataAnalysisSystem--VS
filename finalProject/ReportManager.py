from datetime import datetime

class ReportService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def _execute_query(self, query, params=None):
        try:
            self.db_connection.connect()
            cursor = self.db_connection.get_cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Exception as e:
            print(f"Error during query execution: {e}")
            return []

    def show_all_bill_records_today(self):
        today_date = datetime.today().strftime("%Y-%m-%d")
        query = "SELECT * FROM salesbill WHERE billdate=%s"
        results = self._execute_query(query, (today_date,))

        for x in results:
            print("--------------------------------------")
            print(f'| Bill Code: {x[0]}')
            print(f'| Date: {x[1]}')
            print(f'| Branch: {x[6]}')
            print(f'| User Id: {x[7]}')
            print(f'| Total:                 {x[2]}')
            print(f'| Discount:              {x[3]}')
            print('| ------------------------------------')
            print(f'| Total(After Discount): {x[4]}')
            print("--------------------------------------")
        print("-----------End Search Result-------------")

    def price_analysis(self):
        query = """
        SELECT 
            product.pname, price.productId, price.startDate, price.price,
            LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate) AS previous_price,
            (price.price - LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate)) AS price_change
        FROM price
        INNER JOIN product ON price.productId = product.pcode
        """
        results = self._execute_query(query)

        for x in results:
            print("---------------------------------|")
            print(f'| Product Code: {x[1]}')
            print(f'| Product Name: {x[0]}')
            print(f'| Start Date:   {x[2]}')
            print(f'| Price:        {x[3]}')
            print(f'| Prev. Price:  {x[4]}')
            print("|--------------------------------|")
            print(f'| Price Change: {x[5]}')
            print("|--------------------------------|")
        print("--------------End Report--------------")

    def monthly_sales_analysis(self):
        query = """
        SELECT branchid, YEAR(billdate) AS year, MONTH(billdate) AS month,
               SUM(billTotal) AS total_bill
        FROM salesbill
        GROUP BY branchid, YEAR(billdate), MONTH(billdate)
        ORDER BY branchid, year, month
        """
        results = self._execute_query(query)

        for x in results:
            print("---------------------------------|")
            print(f'| Branch Id:   {x[0]}')
            print(f'| Year:        {x[1]}')
            print(f'| Month:       {x[2]}')
            print("|--------------------------------|")
            print(f'| Total Sales: {x[3]}')
            print("|--------------------------------|")
        print("--------------End Report--------------")

    def weekly_sales_analysis(self):
        query = """
        SELECT salesbill.branchid, branch.branchName,
               YEAR(salesbill.billdate) AS year,
               WEEK(salesbill.billdate) AS week,
               SUM(salesbill.billTotal) AS total_sales
        FROM salesbill
        INNER JOIN branch ON salesbill.branchid = branch.brid
        GROUP BY salesbill.branchid, year, week
        ORDER BY salesbill.branchid, year, week
        """
        results = self._execute_query(query)

        for x in results:
            print("---------------------------------|")
            print(f'| Branch Id:   {x[0]}')
            print(f'| Branch Name: {x[1]}')
            print(f'| Year:        {x[2]}')
            print(f'| Week:        {x[3]}')
            print("|--------------------------------|")
            print(f'| Total Sales: {x[4]}')
            print("|--------------------------------|")
        print("--------------End Report--------------")

    def sales_product_preferences(self):
        query = """
        SELECT si.branchproductid,
               SUM(si.qty) AS total_quantity_sold,
               COUNT(DISTINCT si.billId) AS number_of_sales,
               SUM(si.total) AS total_revenue
        FROM salesitem si
        JOIN salesbill yt ON si.billId = yt.billcode
        GROUP BY si.branchproductid
        ORDER BY total_quantity_sold DESC
        """
        results = self._execute_query(query)

        for x in results:
            print("---------------------------------|")
            print(f'| Branch Product Id:     {x[0]}')
            print(f'| Total Sold Qty:        {x[1]}')
            print(f'| Number of Sales:       {x[2]}')
            print("|--------------------------------|")
            print(f'| Total Revenue:         {x[3]}')
            print("|--------------------------------|")
        print("--------------End Report--------------")

    def final_sales_analysis(self):
        query = """
        SELECT branchid,
               COUNT(billcode) AS number_of_sales,
               SUM(total_sales) AS total_sales_amount,
               AVG(total_sales) AS average_sales_amount,
               MIN(total_sales) AS minimum_sales_amount,
               MAX(total_sales) AS maximum_sales_amount
        FROM (
            SELECT billcode, branchid, SUM(billTotal) AS total_sales
            FROM salesbill
            GROUP BY billcode, branchid
        ) AS sales_per_bill
        GROUP BY branchid
        ORDER BY branchid
        """
        results = self._execute_query(query)

        for x in results:
            print("---------------------------------|")
            print(f'| Branch Id:             {x[0]}')
            print(f'| No. of Sales:          {x[1]}')
            print(f'| Total Sales Amount:    {x[2]}')
            print("|--------------------------------|")
            print(f'| Minimum Sales Amount:  {x[4]}')
            print(f'| Average Sales Amount:  {x[3]}')
            print(f'| Maximum Sales Amount:  {x[5]}')
            print("|--------------------------------|")
        print("--------------End Report--------------")