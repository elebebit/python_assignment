## Project description
This project completes 2 tasks:
- Fetch financial data from an AlphaVantage API , then process the data and put it into the database.
- Offer api to display fetched financial data with page info and  computed statistics with the financial data.

## Tech stack
- Python 3
- Flask
- MySQL
- Docker
- Linux/Unix

## Running the App
**Starting**
```
docker-compose up
```

**Access the financial API app container**
```
docker exec -it container_name bash
```

**Run the Fetch Financial Data Funcion** 
1. Define parameters to the .env file in the root directory for docker compose use.
```
export API_KEY={api_key}
export STOCK_API_URL=https://www.alphavantage.co/query
export APP_DATABASE_URI=mysql://{user}:@app_mysql:{port}/{database_name}
export DB_ROOT_PASSWORD={DB_ROOT_PASSWORD}
export DEFAULT_DB_NAME={DEFAULT_DB_NAME}
```
2. Define parameters to the .env file in the in /final directory
```
SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://{user}:@app_mysql:{port}/{database_name}
```

3. Build corresponding containers.
```
docker-compose up
```

4. Execute get_raw_data.py script and save fetched data in database
```
python get_raw_data.py
```

5. Use Financial Data Api
```
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-02-21&end_date=2023-03-01&symbol=IBM&limit=3&page=1'
```
formatted output:
```
{
  "data": [
    {
      "close_price": "128.19",
      "date": "2023-03-01",
      "open_price": "128.90",
      "symbol": "IBM",
      "volume": "3760678"
    },
    {
      "close_price": "129.30",
      "date": "2023-02-28",
      "open_price": "130.55",
      "symbol": "IBM",
      "volume": "5143133"
    },
    {
      "close_price": "130.49",
      "date": "2023-02-27",
      "open_price": "131.42",
      "symbol": "IBM",
      "volume": "2761326"
    }
  ],
  "info": {
    "error": ""
  },
  "pagination": {
    "count": 7,
    "limit": 3,
    "page": 1,
    "pages": 3
  }
}
```

5. Use Statistics Data Api
```
curl -X GET 'http://localhost:5000/api/statistics?start_date=2023-02-21&end_date=2023-03-06&symbol=IBM'
```
formatted output:
```
{
  "data": {
    "average_daily_close_price": 130.07,
    "average_daily_open_price": 130.63,
    "average_daily_volume": 3562736,
    "end_date": "2023-03-06",
    "start_date": "2023-02-21",
    "symbol": "IBM"
  },
  "info": {
    "error": ""
  }
}
```

6. Stop the application.
```
docker-compose down
```

## How to maintain the API key
- Use API key as environment variable configuration instead of saving it in public environment.
- Set different API keys for production and development environments.
- Deploy the application on the cloud and use extra safe strategy.