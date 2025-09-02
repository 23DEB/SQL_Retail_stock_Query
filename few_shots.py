# few_shots.py

# This file contains the few-shot learning examples for the SQL chain.
# These examples guide the language model to produce better and more accurate SQL queries.

few_shots = [
    {
        "Question": "How many t-shirts do we have left for Nike in XS size and white color?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        "SQLResult": "Result of the SQL query",
        "Answer": "The total stock for Nike t-shirts in XS size and white color is [some_number].",
    },
    {
        "Question": "How much is the total price of the inventory for all S-size t-shirts?",
        "SQLQuery": "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        "SQLResult": "Result of the SQL query",
        "Answer": "The total price of inventory for all small size T-shirts is 19117.",
    },
    {
        "Question": "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?",
        "SQLQuery": """
SELECT sum(a.total_amount * ((100-COALESCE(d.pct_discount,0))/100)) as total_revenue
FROM (
    SELECT sum(price*stock_quantity) as total_amount, t_shirt_id
    FROM t_shirts
    WHERE brand = 'Levi'
    GROUP BY t_shirt_id
) a
LEFT JOIN discounts d ON a.t_shirt_id = d.t_shirt_id
""",
        "SQLResult": "Result of the SQL query",
        "Answer": "The total revenue from Levi t-shirts, after applying discounts, is 19126.10.",
    },
    {
        "Question": "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
        "SQLResult": "Result of the SQL query",
        "Answer": "The total value of Levi t-shirts in stock is 20581.",
    },
    {
        "Question": "How many white color Levi's shirts do I have?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
        "SQLResult": "Result of the SQL query",
        "Answer": "There are 100 white Levi's shirts available.",
    },
]
