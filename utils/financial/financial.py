import re
import requests
import yfinance as yf
from datetime import datetime
import jdatetime
from datetime import timedelta,datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import streamlit as st
import json
import os

script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
keywords_path = os.path.join(script_dir, "data","Financial_keywords.json")

with open(keywords_path, "r", encoding="utf-8") as f:
    
    keywords = json.load(f)
    currency_keywords = keywords["currency_keywords"]
    gold_keywords = keywords["gold_keywords"]
    stock_keywords = keywords["stock_keywords"]
    american_stock_symbols_keywords = keywords["american_stock_symbols_keywords"]
    index_symbols_keywords = keywords["index_symbols_keywords"]
    cryptocurrency_keywords = keywords["cryptocurrency_keywords"]
    iran_symbols_keywords = keywords["iran_symbols_keywords"]
    time_keywords = keywords["time_keywords"]

def extract_features(user_input):
    """Extract financial features from user input."""
    extracted_features = {}

    for word in currency_keywords:
        if word in user_input:
            extracted_features["type"] = "currency"
            extracted_features["symbol"] = word
            break

    for word in gold_keywords:
        if word in user_input:
            extracted_features["type"] = "gold"
            extracted_features["symbol"] = word
            break

    stock_keywords_founded = False
    for word in stock_keywords:
        if word in user_input:
            extracted_features["type"] = "stock"
            for words in american_stock_symbols_keywords:
                if words in user_input:
                    extracted_features["sub_type"] = "America Stock"
                    extracted_features["symbol"] = words
                    stock_keywords_founded = True
                    break

            if not stock_keywords_founded:
                for words in index_symbols_keywords:
                    if words in user_input:
                        extracted_features["sub_type"] = "Iran Index"
                        extracted_features["symbol"] = words
                        stock_keywords_founded = True
                        break

            if not stock_keywords_founded:
                for words in iran_symbols_keywords:
                    if words in user_input:
                        extracted_features["sub_type"] = "Iran Symbol"
                        extracted_features["symbol"] = words
                        stock_keywords_founded = True
                        break

    for word in cryptocurrency_keywords:
        if word in user_input:
            extracted_features["type"] = "cryptocurrency"
            extracted_features["symbol"] = word
            break

    for word, value in time_keywords.items():
        if word in user_input:
            extracted_features["time"] = value
            break
    if "time" not in extracted_features:
        extracted_features["time"] = "today"  # Default Value

    if "تغییر" in user_input:
        extracted_features["Change_Command"] = True
    else:
        extracted_features["Change_Command"] = False

    if not stock_keywords_founded:
        extracted_features["sub_type"] = "Iran Symbol"

    return extracted_features

# Current Price Functions
def get_currency_price_tgju(input_currency):
    """Fetch current currency price from tgju.org."""
    
    current_price = None
    change_percentage = None
    percent_change = None
    is_positive = None

    currencys = {
        "دلار": "https://www.tgju.org/profile/price_dollar_rl",
        "یورو": "https://www.tgju.org/profile/price_eur",
        "پوند": "https://www.tgju.org/profile/price_gbp",
        "درهم": "https://www.tgju.org/profile/price_aed",
        "دینار": "https://www.tgju.org/profile/price_kwd",
        "فرانک": "https://www.tgju.org/profile/price_chf",
        "روبل": "https://www.tgju.org/profile/price_rub",
    }

    currency_link = currencys.get(input_currency)
    if not currency_link:
        return "ارز وارد شده معتبر نیست."

    response = requests.get(currency_link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table table-hover text-center")

        if table:
            rows = table.find_all("tr")  

            prices = {}
            for row in rows:
                cols = row.find_all("td")

                header = ""
                value = ""
                if len(cols) > 1:

                    header = cols[0].text.strip()
                    value = cols[1]

                if header == "نرخ فعلی":
                    current_price = int(float(value.text.replace(",","").strip()) / 10)
                    current_price = "{:,}".format(current_price)

                elif header == "درصد تغییر نسبت به روز گذشته":
                            
                    span = value.find("span")

                    if span:
                                
                        change_percentage = float(span.text.strip().replace('%', ''))
                        is_positive = 'high' in span.get('class', [])

                    else:
                        change_percentage = float(value.text.strip().replace('%', ''))
                    
                    if not is_positive:  
                        change_percentage *= -1                

        else:
            print("Couldn't find the table.")    

    return f"قیمت {input_currency} امروز {current_price} تومان است و {abs(change_percentage)} درصد تغییر داشته که نسبت به دیروز {'افزایش' if change_percentage > 0 else 'کاهش'} یافته است."


def get_gold_price_tgju(input_gold):
    """Fetch current gold price from tgju.org."""
    
    current_price = None
    change_percentage = None
    percent_change = None
    is_positive = None
    

    gold_types = {
        "طلا": "https://www.tgju.org/profile/ons",
        "سکه امامی": "https://www.tgju.org/profile/sekee",
        "سکه بهار آزادی": "https://www.tgju.org/profile/sekeb",
        "ربع سکه": "https://www.tgju.org/profile/rob",
        "نیم سکه": "https://www.tgju.org/profile/nim",
        "سکه": "https://www.tgju.org/profile/sekee",
    }

    gold_link = gold_types.get(input_gold)

    if not gold_link:
        return "طلا وارد شده معتبر نیست."

    response = requests.get(gold_link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", class_="table table-hover text-center")

        if table:
            rows = table.find_all("tr")  

            for row in rows:
                cols = row.find_all("td")

                header = ""
                value = ""

                if len(cols) > 1:
        
                    header = cols[0].text.strip()
                    value = cols[1]

                if header == "نرخ فعلی":
                    current_price = int(float(value.text.replace(",","").strip()) / 10)
                    current_price = "{:,}".format(current_price)

                elif header == "درصد تغییر نسبت به روز گذشته":
                            
                    span = value.find("span")

                    if span:
                                
                        change_percentage = float(span.text.strip().replace('%', ''))
                        is_positive = 'high' in span.get('class', [])

                    else:
                        change_percentage = float(value.text.strip().replace('%', ''))
                    
                    if not is_positive:  
                        change_percentage *= -1   

        else:
            print("Couldn't find the table.")    

    return f"قیمت {input_gold} امروز {current_price} تومان است و {abs(change_percentage)} درصد تغییر داشته که نسبت به دیروز {'افزایش' if change_percentage > 0 else 'کاهش'} یافته است."


def get_cryptocurrency_price_tgju(input_cryptocurrency):
    """Fetch current cryptocurrency price from tgju.org."""
    
    current_price = None
    change_percentage = None
    percent_change = None
    is_positive = None

    cryptocurrencies = {
        "بیت کوین": "https://www.tgju.org/profile/crypto-bitcoin",
        "اتریوم": "https://www.tgju.org/profile/crypto-ethereum",
        "کاردانو": "https://www.tgju.org/profile/crypto-cardano",
        "ریپل": "https://www.tgju.org/profile/crypto-ripple",
        "تتر گلد": "https://www.tgju.org/profile/crypto-tether-gold"
    }

    cryptocurrency_link = cryptocurrencies.get(input_cryptocurrency)

    if not cryptocurrency_link:
        return "ارز دیجیتال وارد شده معتبر نیست."

    response = requests.get(cryptocurrency_link)

    if response.status_code == 200:
                
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table table-hover text-center")

        if table:
            rows = table.find_all("tr")  
            for row in rows:
                cols = row.find_all("td")

                header = ""
                value = ""                             

                if len(cols) > 1:

                    header = cols[0].text.strip()
                    value = cols[1]

                if header == "نرخ فعلی":

                    current_price = round(float(value.text.replace(",","").strip()),2)
                    current_price = "{:,}".format(current_price)

                elif header == "قیمت ریالی":

                    rials_price = int(float(value.text.replace(",","").strip()) / 10)
                    rials_price = "{:,}".format(rials_price)

                elif header == "درصد تغییر نسبت به روز گذشته":

                    span = value.find("span")

                    if span:

                        change_percentage = float(span.text.strip().replace('%', ''))
                        is_positive = 'high' in span.get('class', [])

                    else:
                        change_percentage = float(value.text.strip().replace('%', ''))

                    if not is_positive:  
                        change_percentage *= -1  

        else:
            print("Couldn't find the table.")    

    return f"قیمت {input_cryptocurrency} امروز {current_price} دلار و معادل {rials_price}   تومان است  و{abs(change_percentage)} درصد تغییر داشته که نسبت به دیروز {'افزایش' if change_percentage > 0 else 'کاهش'} یافته است."

def get_america_stock_price(input_company):
    """Fetch current American stock price from Alpha Vantage."""
     
    companies = {
        "اپل": "AAPL",
        "گوگل": "GOOGL",
        "آمازون": "AMZN",
        "مایکروسافت": "MSFT",
        "تسلا": "TSLA",
    }

    symbol = companies.get(input_company)
    if not symbol:
        return "❌ نام شرکت معتبر نیست!"

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": "ZQ13T44C9S0C2G4M",
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "Time Series (Daily)" not in data:
            return f"⛔️ داده‌ای برای نماد {symbol} پیدا نشد یا API محدود شده."

        time_series = data["Time Series (Daily)"]
        sorted_dates = sorted(time_series.keys(), reverse=True)

        if len(sorted_dates) < 2:
            return "⛔️ تعداد روزهای معاملاتی کافی نیست."

        today = sorted_dates[0]
        yesterday = sorted_dates[1]

        today_close = float(time_series[today]["4. close"])
        yesterday_close = float(time_series[yesterday]["4. close"])

        change_percent = ((today_close - yesterday_close) / yesterday_close) * 100

        return (
            f"قیمت پایانی سهام {input_company} ({symbol}) در تاریخ {today}، "
            f"{today_close:.2f} دلار بوده است.\n"
            f"{'که افزایش' if change_percent > 0 else 'که کاهش'} {abs(change_percent):.2f}% نسبت به روز قبل داشته است."
        )

    except Exception as e:
        return f"❌ خطا در دریافت یا پردازش اطلاعات: {e}"

def get_iran_index_data(input_index):
    """Fetch current Iranian index data from BrsApi."""
    api_key = "FreeBvt6cnOYtMgfj8GQP5GSuIy8LUh5"
    type = "1"

    if input_index in ["شاخص کل", "شاخص بورس"]:
        type = "3"
    elif input_index == "شاخص فرابورس":
        type = "2"
    else:
        type = "3"

    url = "https://BrsApi.ir/Api/Tsetmc/Index.php?key=" + api_key + "&type=" + type

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if input_index in ["شاخص کل", "شاخص بورس"]:
            for index in data:

                name = index["name"]
                if name == "شاخص کل":

                    index_price = "{:,}".format(float(index["index"]))
                    price_change_percentage = index["index_change_percent"]
                    return f"{input_index} برابر {index_price} است و {abs(price_change_percentage)} درصد تغییر داشته که نسبت به دیروز {'افزایش' if price_change_percentage > 0 else 'کاهش'} یافته است."

        if input_index == "شاخص فرابورس":
            index_price = "{:,}".format(float(data["index"]))
            date = data["date"]
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
            price_change_percentage = data["index_change"]
            return f"{input_index} در تاریخ {formatted_date} برابر {index_price} است که نسبت به دیروز {price_change_percentage}  تغییر داشته"

        else:

            for index in data:

                name = index["name"]
                if name == "شاخص کل (هم وزن)":

                    index_price = "{:,}".format(float(index["index"]))
                    price_change_percentage = index["index_change_percent"]
                    return f"{input_index} برابر {index_price} است و {abs(price_change_percentage)} درصد تغییر داشته که نسبت به دیروز {'افزایش' if price_change_percentage > 0 else 'کاهش'} یافته است."


def get_iran_symbol_data(input_symbol):
    """Fetch current Iranian symbol data from BrsApi."""
    
    api_key = "FreeBvt6cnOYtMgfj8GQP5GSuIy8LUh5"
    url = "https://BrsApi.ir/Api/Tsetmc/AllSymbols.php?key=" + api_key

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
        "Accept": "application/json, text/plain, */*",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        for symbols in data:
            symbol_name = symbols["l18"]
            company_name = symbols["l30"]
            price = "{:,}".format(int(symbols["pc"]) / 10)
            price_change_percentage = symbols["pcp"]

            if symbol_name == input_symbol:
                return f"قیمت نماد {input_symbol} برابر {price} تومان است و {abs(price_change_percentage)} درصد تغییر داشته که نسبت به دیروز {'افزایش' if price_change_percentage > 0 else 'کاهش'} یافته است."
    else:

        return f"Error: {response.status_code}"

# Historical Price Functions
def get_time_period_persian(input_time):
    """Convert time period to Persian date format."""
    
    today = jdatetime.date.today()

    if input_time == "yesterday":
        time = today - timedelta(days=1)
        return f"{time.year}/{time.month:02d}/{time.day:02d}"

    elif input_time == "last_week":
        time = today - timedelta(weeks=1)
        return f"{time.year}/{time.month:02d}/{time.day:02d}"

    elif input_time == "last_month":
        if today.month > 1:
            time = today.replace(month=today.month - 1)
        else:
            time = today.replace(year=today.year - 1, month=12)
        return f"{time.year}/{time.month:02d}/{time.day:02d}"

    elif input_time == "last6_months":
        if today.month > 6:
            time = today.replace(month=today.month - 6)
        else:
            time = today.replace(year=today.year - 1, month=today.month + 6)
        return f"{time.year}/{time.month:02d}/{time.day:02d}"

    elif input_time == "last_year":
        time = today.replace(year=today.year - 1)
        return f"{time.year}/{time.month:02d}/{time.day:02d}"

    elif input_time == "last3_year":
        time = today.replace(year=today.year - 3)
        return f"{time.year}/{time.month:02d}/{time.day:02d}"

    else:
        return "ورودی نامعتبر"


def get_past_date(time_period):
    """Convert time period to Gregorian date format."""
    
    today = datetime.today()
    date_format = "%Y/%m/%d"

    if time_period == "yesterday":
        past_date = today - relativedelta(days=1)
    elif time_period == "last_week":
        past_date = today - relativedelta(weeks=1)
    elif time_period == "last_month":
        past_date = today - relativedelta(months=1)
    elif time_period == "last6_months":
        past_date = today - relativedelta(months=6)
    elif time_period == "last_year":
        past_date = today - relativedelta(years=1)
    elif time_period == "last3_year":
        past_date = today - relativedelta(years=3)
    else:
        return "بازه زمانی نامعتبر است!"

    return past_date.strftime(date_format)


def get_history_currency_price(input_currency, input_time):
    """Find the closest date to target_date from a list of dates."""
    
    price = ""
    date = ""

    time = get_past_date(input_time)

    currencys = {
        "دلار": "https://www.tgju.org/profile/price_dollar_rl/history",
        "یورو": "https://www.tgju.org/profile/price_eur/history",
        "پوند": "https://www.tgju.org/profile/price_gbp/history",
        "درهم": "https://www.tgju.org/profile/price_aed/history",
        "دینار": "https://www.tgju.org/profile/price_kwd/history",
        "فرانک": "https://www.tgju.org/profile/price_chf/history",
    }

    currency_link = currencys.get(input_currency)
    if not currency_link:
       return "ارز وارد شده معتبر نیست."

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(currency_link, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        td_tag = soup.find("td", string=time)

        if not td_tag:
            all_dates = [
                td.text.strip()
                for td in soup.find_all("td")
                if td.text.strip().count("/") == 2
            ]
            closest_time = find_closest_date(all_dates, time)
            if closest_time:
                td_tag = soup.find("td", string=closest_time)
                time = closest_time
            else:
                return "تاریخ مشابهی در داده‌ها پیدا نشد."

        if td_tag:
            tr_tag = td_tag.find_parent("tr")

            td_elements = tr_tag.find_all("td")
            if len(td_elements) >= 8:
                close_price = int(td_elements[3].text.strip().replace(",", ""))
                close_price = "{:,}".format(close_price // 10)
                price = close_price
                date = td_elements[7].text.strip()

                return f"قیمت {input_currency} در تاریخ {date}، {price} تومان بود."
            else:
                return "اطلاعات کافی برای این تاریخ موجود نیست."

    return f"قیمت {input_currency} در تاریخ {date}، {price} تومان بود."


def find_closest_date(dates, target_date):
    """
    دریافت لیست تاریخ‌های موجود در صفحه و پیدا کردن نزدیک‌ترین تاریخ به `target_date`.
    """
    date_format = "%Y/%m/%d"
    target_date = datetime.strptime(target_date, date_format)

    closest_date = None
    min_diff = float("inf")

    for date_str in dates:
        try:
            current_date = datetime.strptime(date_str, date_format)
            diff = abs((target_date - current_date).days)

            if diff < min_diff and current_date <= target_date:
                min_diff = diff
                closest_date = date_str
        except ValueError:
            continue

    return closest_date

def get_history_gold_price(input_gold, input_time):
    """Fetch historical gold price from tgju.org."""
    
    price = ""
    date = ""

    time = get_past_date(input_time)

    gold_types = {
        "طلا": "https://www.tgju.org/profile/ons/history",
        "سکه امامی": "https://www.tgju.org/profile/sekee/history",
        "سکه بهار آزادی": "https://www.tgju.org/profile/sekeb/history",
        "ربع سکه": "https://www.tgju.org/profile/rob/history",
        "نیم سکه": "https://www.tgju.org/profile/nim/history",
        "سکه": "https://www.tgju.org/profile/sekee/history",
    }

    gold_link = gold_types.get(input_gold)
    if not gold_link:
        return "نوع طلای وارد شده معتبر نیست."

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(gold_link, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        td_tag = soup.find("td", string=time)

        if not td_tag:
            all_dates = [
                td.text.strip()
                for td in soup.find_all("td")
                if td.text.strip().count("/") == 2
            ]
            closest_time = find_closest_date(all_dates, time)
            if closest_time:
                td_tag = soup.find("td", string=closest_time)
                time = closest_time
            else:
                return "تاریخ مشابهی در داده‌ها پیدا نشد."

        if td_tag:
            tr_tag = td_tag.find_parent("tr")

            td_elements = tr_tag.find_all("td")
            if len(td_elements) >= 8:
                close_price = int(td_elements[3].text.strip().replace(",", "")) / 10
                close_price = "{:,}".format(close_price)
                price = close_price
                date = td_elements[7].text.strip()

                return f"قیمت {input_gold} در تاریخ {date}، {price} تومان بود."
            else:
                return "اطلاعات کافی برای این تاریخ موجود نیست."

    return f"خطا در دریافت داده‌ها: {response.status_code}"


def get_history_cryptocurrency_price(input_cryptocurrency, input_time):
    """Fetch historical cryptocurrency price from tgju.org."""
    
    price = ""
    date = ""

    time = get_past_date(input_time)

    cryptocurrencies = {
        "بیت کوین": "https://www.tgju.org/profile/crypto-bitcoin/history",
        "اتریوم": "https://www.tgju.org/profile/crypto-ethereum/history",
        "کاردانو": "https://www.tgju.org/profile/crypto-cardano/history",
    }

    crypto_link = cryptocurrencies.get(input_cryptocurrency)
    if not crypto_link:
        return "ارز دیجیتال وارد شده معتبر نیست."

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(crypto_link, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        td_tag = soup.find("td", string=time)

        if not td_tag:
            all_dates = [
                td.text.strip()
                for td in soup.find_all("td")
                if td.text.strip().count("/") == 2
            ]
            closest_time = find_closest_date(all_dates, time)
            if closest_time:
                td_tag = soup.find("td", string=closest_time)
                time = closest_time
            else:
                return "تاریخ مشابهی در داده‌ها پیدا نشد."

        if td_tag:
            tr_tag = td_tag.find_parent("tr")

            td_elements = tr_tag.find_all("td")
            if len(td_elements) >= 8:
                try:
                    close_price = float(td_elements[3].text.strip().replace(",", ""))
                    price = "{:,.2f}".format(close_price)
                except ValueError:
                    return "قیمت معتبر پیدا نشد."

                date = td_elements[7].text.strip()

                return f"قیمت {input_cryptocurrency} در تاریخ {date}، {price} دلار بود."
            else:
                return "اطلاعات کافی برای این تاریخ موجود نیست."

    return f"خطا در دریافت داده‌ها: {response.status_code}"


def get_history_iran_index_price(input_index, input_time):
    """Fetch historical Iranian symbol price from BrsApi."""
    price = ""
    date = ""

    time = get_time_period_persian(input_time)

    indexs = {
        "شاخص کل": "https://www.shakhesban.com/markets/index/%D8%B4-%DA%A9%D9%84-%D8%A8%D9%88%D8%B1%D8%B3/history",
        "شاخص بورس": "https://www.shakhesban.com/markets/index/%D8%B4-%DA%A9%D9%84-%D8%A8%D9%88%D8%B1%D8%B3/history",
        "شاخص فرابورس": "https://www.shakhesban.com/markets/index/%D8%B4-%DA%A9%D9%84-%D9%81%D8%B1%D8%A7%D8%A8%D9%88%D8%B1%D8%B3/history",
        "شاخص هم وزن": "https://www.shakhesban.com/markets/index/%D8%B4-%DA%A9%D9%84-%D9%87%D9%85-%D9%88%D8%B2%D9%86/history",
    }

    index_link = indexs.get(input_index)
    if not index_link:
        return "شاخص وارد شده معتبر نیست."

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(index_link, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        td_tag = soup.find("td", string=time)

        if not td_tag:
            all_dates = [
                td.text.strip()
                for td in soup.find_all("td")
                if td.text.strip().count("/") == 2
            ]
            closest_time = find_closest_date(all_dates, time)
            if closest_time:
                td_tag = soup.find("td", string=closest_time)
                time = closest_time
            else:
                return "تاریخ مشابهی در داده‌ها پیدا نشد."

        if td_tag:
            tr_tag = td_tag.find_parent("tr")

            td_elements = tr_tag.find_all("td")
            if len(td_elements) >= 3:
                try:
                    raw_price = (
                        td_elements[1].text.strip().replace("میلیون", "").strip()
                    )

                    if input_index in ["شاخص کل", "شاخص بورس"]:
                        close_price = float(raw_price) * 1000000
                    else:
                        close_price = float(raw_price.replace(",", ""))

                    price = "{:,}".format(close_price)
                except ValueError:
                    return "قیمت معتبر پیدا نشد."

                date = td_elements[0].text.strip()

                return f"{input_index} در تاریخ {date} برابر {price} بود."
            else:
                return "اطلاعات کافی برای این تاریخ موجود نیست."

    return f"خطا در دریافت داده‌ها: {response.status_code}"


def get_history_iran_symbol_price(input_symbol, input_time):

    api_key = "FreeBvt6cnOYtMgfj8GQP5GSuIy8LUh5"
    url = (
        "https://BrsApi.ir/Api/Tsetmc/History.php?key="
        + api_key
        + "&type=0&l18="
        + input_symbol
    )
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
        "Accept": "application/json, text/plain, */*",
    }

    time = get_time_period_persian(input_time)
    time = time.replace("/", "-")
    print(time)

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        for symbol_price in data:
            symbol_date = symbol_price["date"]
            # print(symbol_date)

            if symbol_date == time:
                price = "{:,}".format(int(symbol_price["pc"]) / 10)
                print(price)
                # return f"{input_index} در تاریخ {date} برابر {price} بود."
                return f"قیمت نماد {input_symbol}  در تاریخ {symbol_date} برابر {price} بود"
    else:

        return f"Error: {response.status_code}"


def get_america_stock_price_change(symbol, input_time, changed_command):
    """Fetch American stock price change from Alpha Vantage."""
    
    API_KEY = "ZQ13T44C9S0C2G4M"
    companies = {
        "اپل": "AAPL",
        "گوگل": "GOOG",
        "آمازون": "AMZN",
        "مایکروسافت": "MSFT",
        "تسلا": "TSLA",
    }

    time_map = {
        "yesterday": ("دیروز", 1),
        "last_week": ("یک هفته", 7),
        "last_month": ("یک ماه", 30),
        "last6_months": ("شش ماه", 180),
        "last_year": ("یک سال", 365),
        "last3_year": ("سه سال", 1095),
    }

    if input_time not in time_map:
        return "بازه زمانی نامعتبر است."

    fa_time, days_ago = time_map[input_time]
    company_symbol = companies.get(symbol, None)
    if not company_symbol:
        return "شرکت وارد شده نامعتبر است."

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company_symbol}&apikey={API_KEY}&outputsize=full"
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        return f"⛔️ اطلاعاتی برای نماد {symbol} پیدا نشد."

    time_series = data["Time Series (Daily)"]
    dates = sorted(time_series.keys(), reverse=True)

    today_close = None
    past_close = None

    for date_str in dates:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if not today_close:
            today_close = float(time_series[date_str]["4. close"])
        if date_obj <= datetime.now() - timedelta(days=days_ago):
            past_close = float(time_series[date_str]["4. close"])
            break

    if not past_close:
        return f"⛔️ قیمت مربوط به {fa_time} پیش یافت نشد."

    price_change = ((today_close - past_close) / past_close) * 100

    if changed_command:
        return f"قیمت سهام {symbol} {abs(price_change):.2f} درصد تغییر داشته که نسبت به {fa_time} پیش {'افزایش' if price_change > 0 else 'کاهش'} یافته است."
    else:
        return f"قیمت سهام {symbol} {fa_time} پیش {past_close:.2f} دلار بود."


def get_currency_change(input_currency, input_time):
    """Fetch currency price change from tgju.org."""
    
    time_map = {
        "yesterday": "دیروز",
        "last_week": "یک هفته",
        "last_month": "یک ماه",
        "last6_months": "شش ماه",
        "last_year": "یک سال",
        "last3_year": "سه سال",
    }

    period_fa = time_map.get(input_time, None)
    if period_fa is None:
        return "⛔ بازه زمانی نامعتبر است."

    currencys = {
        "دلار": "https://www.tgju.org/profile/price_dollar_rl",
        "یورو": "https://www.tgju.org/profile/price_eur",
        "پوند": "https://www.tgju.org/profile/price_gbp",
        "درهم": "https://www.tgju.org/profile/price_aed",
        "دینار": "https://www.tgju.org/profile/price_kwd",
        "فرانک": "https://www.tgju.org/profile/price_chf",
    }

    url = currencys.get(input_currency)
    if not url:
        return "⛔ ارز وارد شده معتبر نیست."

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"⛔ خطا در دریافت داده‌ها: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("div.profile-performance-box table tbody tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        period = cells[0].text.strip()
        if period != period_fa:
            continue

        price_change = cells[1].text.strip().replace(",", "")
        
        percent_span = cells[2].find("span")
        percent_text = percent_span.text.strip().replace("%", "")
        percent_value = round(float(percent_text), 2)

        direction = "افزایش" if "high" in percent_span.get("class", []) else "کاهش"
        
        date = cells[3].text.strip()

        return f"در بازه‌ی {period} تا تاریخ {date}، قیمت {input_currency} {direction} یافته و {percent_value} درصد تغییر کرده است."

    return f"⛔ اطلاعاتی برای بازه‌ی «{period_fa}» یافت نشد."

def get_gold_change(input_gold, input_time):
            
    time_map = {
        "yesterday": "دیروز",
        "last_week": "یک هفته",
        "last_month": "یک ماه",
        "last6_months": "شش ماه",
        "last_year": "یک سال",
        "last3_year": "سه سال",
    }

    period_fa = time_map.get(input_time, None)
    if period_fa is None:
        return "⛔ بازه زمانی نامعتبر است."

    gold_items = {
        "طلا": "https://www.tgju.org/profile/ons",
        "سکه امامی": "https://www.tgju.org/profile/sekee",
        "سکه بهار آزادی": "https://www.tgju.org/profile/sekeb",
        "ربع سکه": "https://www.tgju.org/profile/rob",
        "نیم سکه": "https://www.tgju.org/profile/nim",
        "سکه": "https://www.tgju.org/profile/sekee",
    }

    url = gold_items.get(input_gold)
    if not url:
        return "⛔ نوع طلا یا سکه وارد شده معتبر نیست."

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"⛔ خطا در دریافت داده‌ها: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("div.profile-performance-box table tbody tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        period = cells[0].text.strip()
        if period != period_fa:
            continue

        price_change = cells[1].text.strip().replace(",", "")
        percent_span = cells[2].find("span")
        percent_value = round(float(percent_span.text.strip().replace("%", "")), 2)
        direction = "افزایش" if "high" in percent_span.get("class", []) else "کاهش"
        date = cells[3].text.strip()

        return f"در بازه‌ی {period} تا تاریخ {date}، قیمت {input_gold} {direction} یافته و {percent_value} درصد تغییر کرده است."

    return f"⛔ اطلاعاتی برای بازه‌ی «{period_fa}» یافت نشد."

def get_cryptocurrency_change(input_cryptocurrency, input_time):
            
    time_map = {
        "yesterday": "دیروز",
        "last_week": "یک هفته",
        "last_month": "یک ماه",
        "last6_months": "شش ماه",
        "last_year": "یک سال",
        "last3_year": "سه سال",
    }

    period_fa = time_map.get(input_time, None)
    if period_fa is None:
        return "⛔ بازه زمانی نامعتبر است."

    crypto_items = {
        "بیت کوین": "https://www.tgju.org/profile/crypto-bitcoin",
        "اتریوم": "https://www.tgju.org/profile/crypto-ethereum",
        "کاردانو": "https://www.tgju.org/profile/crypto-cardano",
    }

    url = crypto_items.get(input_cryptocurrency)
    if not url:
        return "⛔ نام رمزارز وارد شده معتبر نیست."

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"⛔ خطا در دریافت داده‌ها: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("div.profile-performance-box table tbody tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        period = cells[0].text.strip()
        if period != period_fa:
            continue

        price_change = cells[1].text.strip().replace(",", "")
        percent_span = cells[2].find("span")
        percent_value = round(float(percent_span.text.strip().replace("%", "")), 2)
        direction = "افزایش" if "high" in percent_span.get("class", []) else "کاهش"
        date = cells[3].text.strip()

        return f"در بازه‌ی {period} تا تاریخ {date}، قیمت {input_cryptocurrency} {direction} یافته و {percent_value} درصد تغییر کرده است."

    return f"⛔ اطلاعاتی برای بازه‌ی «{period_fa}» یافت نشد."


def process_request(user_input):

    features = extract_features(user_input)

    if features["type"] == "currency":

        if features["time"] == "today":
            return get_currency_price_tgju(features["symbol"])

        elif features["Change_Command"]:
            return get_currency_change(features["symbol"], features["time"])

        else:        
            return get_history_currency_price(features["symbol"], features["time"])


    elif features["type"] == "gold":

        if features["time"] == "today":
            return get_gold_price_tgju(features["symbol"])

        elif features["Change_Command"]:
            return get_gold_change(features["symbol"], features["time"])

        else:
            return get_history_gold_price(features["symbol"], features["time"])

    elif features["type"] == "stock":

        if features["sub_type"] == "America Stock":

            if features["time"] == "today":
                return get_america_stock_price(features["symbol"])

            elif features["Change_Command"]:
                return get_america_stock_price_change(
                    features["symbol"], features["time"], True
                )

            else:
                return get_america_stock_price_change(
                    features["symbol"], features["time"], False
                )

        elif features["sub_type"] == "Iran Index":

            if features["time"] == "today":
                return get_iran_index_data(features["symbol"])

            else:
                return get_history_iran_index_price(
                    features["symbol"], features["time"]
                )

        else:

            features["sub_type"] == "Iran Symbol"

            if features["symbol"] is None:

                symbol_name = input("Enter your Symbol Name Again Please : ")
                return get_iran_symbol_data(symbol_name)

            else:
                if features["time"] == "today":
                    return get_iran_symbol_data(features["symbol"])
                else:
                    return get_history_iran_symbol_price(
                        features["symbol"], features["time"]
                    )

    elif features["type"] == "cryptocurrency":

        if features["time"] == "today":
            return get_cryptocurrency_price_tgju(features["symbol"])

        elif features["Change_Command"]:
            return get_cryptocurrency_change(features["symbol"], features["time"])

        else:
            return get_history_cryptocurrency_price(
                features["symbol"], features["time"]
            )

    else:
        return "نوع درخواست مشخص نیست!"

def run(command,iom):
    try:
        result = process_request(command)
        print(result)
        iom.getSpeaker().say(result)

    except Exception as e:

        print("خطا در اجرای تحلیل سوال:", e)
        iom.getSpeaker().say("مشکلی در تحلیل سوال پیش آمد.")

def main():
    st.set_page_config(page_title="چت‌بات مالی", page_icon="💰", layout="centered")

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #2c3e50;
                color: white;
                direction: rtl;
                text-align: right;
            }
            .title {
                text-align: center;
                font-size: 32px;
                color: #f1c40f;
                font-weight: bold;
            }
            .input-box {
                border: 2px solid #f39c12;
                padding: 12px;
                border-radius: 10px;
                background-color: #34495e;
                color: white;
                direction: rtl;
                text-align: right;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1 class='title'>💰 چت‌بات مالی 💰</h1>", unsafe_allow_html=True)
    user_query = st.text_input(
        "🔍 درخواست خود را وارد کنید:", key="query", help="مثلاً: قیمت دلار امروز چنده؟"
    )
    if user_query:

        chatpot_respond = process_request(user_query)
        st.success(f"📊 {chatpot_respond}")


if __name__ == "__main__":
    main()
