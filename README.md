# T-Shirt SQL Query Assistant

A Streamlit application that allows users to ask questions about t-shirt inventory in plain English and get SQL-generated answers.

## Features

- Natural language to SQL query conversion
- Real-time inventory queries
- Interactive web interface
- Secure credential management

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Update `.streamlit/secrets.toml` with your credentials:
```toml
[database]
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_HOST = "your_db_host"
DB_NAME = "your_db_name"

[api]
GOOGLE_API_KEY = "your_google_api_key"
```

3. Run the application:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Connect your GitHub repo to Streamlit Cloud
3. Add secrets in Streamlit Cloud dashboard under "Secrets"
4. Deploy!

## Database Setup

Ensure your MySQL database is accessible and contains the required tables:
- `t_shirts` (with columns: brand, color, size, stock_quantity, price, t_shirt_id)
- `discounts` (with columns: t_shirt_id, pct_discount)