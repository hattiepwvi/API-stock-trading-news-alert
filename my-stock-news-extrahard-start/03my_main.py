import requests
import datetime
import vonage
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "balibulibong"
NEWS_API_KEY ="balibulibong"


def text():
    for article in articles:
        return f"Headline: {article['title']}\nBrief: {article['description']}\n"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

if diff_percent > 5:
    print("Get News")
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    response = requests.get(NEWS_ENDPOINT, params=news_params)

    articles = response.json()["articles"][:3]

    print(articles)

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    if yesterday_closing_price > day_before_yesterday_closing_price:
        percent = f"🔺{diff_percent}"
    else:
        percent = f"🔻{diff_percent}"
    print(percent)


    # print(articles[0]["title"], articles[0]["description"])

    client = vonage.Client(key="balibulibong", secret="balibulibong")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "86balibulibong",
            "text": f"TSLA: {percent}\n{text()}",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

