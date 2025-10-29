from dataclasses import dataclass
import requests
import urllib.parse
import tkinter as tk
import datetime
import re
import difflib
from typing import Optional

PERSIAN_NUMBER_WORDS = {
    "یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5,
    "شش": 6, "هفت": 7, "هشت": 8, "نه": 9, "ده": 10
}

def normalize_fa(s: str) -> str:
    
    s = s.replace("ي", "ی").replace("ك", "ک").replace("ۀ", "ه")
    s = s.replace("\u200c", "")  
    s = s.replace("\u0640", "")  
    s = re.sub(r"[\u064B-\u065F]", "", s)  
    return s

@dataclass
class WeatherQuery:
    location: str
    time_range: str
    data_type: str

TIME_KEYWORDS = {
    "now": ["الان", "هم‌اکنون", "فعلاً", "در حال حاضر"],
    "today": ["امروز", "امروزه"],
    "tomorrow": ["فردا", "روز بعد"],
    "week": ["هفته آینده", "هفته بعد", "چند روز آینده"]
}

WEEKDAYS = {
    "شنبه": 5, "یکشنبه": 6, "دوشنبه": 0, "سه‌شنبه": 1,
    "چهارشنبه": 2, "پنجشنبه": 3, "جمعه": 4
}

DATA_TYPE_KEYWORDS = {
    "temperature": ["دمای", "درجه", "گرما", "سرما", "چند درجه", "هوا سرده", "هوا گرمه", "بیشترین دما", "کمترین دما"],
    "rain": ["بارون", "بارندگی", "بارش", "می‌باره", "بارونی"],
    "wind": ["باد", "سرعت باد", "جهت باد", "باد میاد"],
    "storm": ["طوفان", "طوفانی"],
    "humidity": ["رطوبت"],
    "general": ["وضعیت هوا", "هوا چطوره", "آب‌وهوا", "هوا"]
}

CITY_TRANSLATIONS = {
    "تهران": "Tehran", "مشهد": "Mashhad", "اصفهان": "Isfahan", "شیراز": "Shiraz", "رشت": "Rasht",
    "تبریز": "Tabriz", "اهواز": "Ahvaz", "قم": "Qom", "کرمانشاه": "Kermanshah", "کرمان": "Kerman",
    "یزد": "Yazd", "اردبیل": "Ardabil", "زنجان": "Zanjan", "ساری": "Sari", "ارومیه": "Urmia",
    "بندرعباس": "Bandar Abbas", "سنندج": "Sanandaj", "قزوین": "Qazvin", "بوشهر": "Bushehr", "ایلام": "Ilam",
    "شهرکرد": "Shahrekord", "گرگان": "Gorgan", "خرم‌آباد": "Khorramabad", "بیرجند": "Birjand",
    "بجنورد": "Bojnurd", "یاسوج": "Yasuj", "اراک": "Arak", "همدان": "Hamedan", "سمنان": "Semnan",
    "زاهدان": "Zahedan"
}

CITY_TRANSLATIONS_NORM = {normalize_fa(k): v for k, v in CITY_TRANSLATIONS.items()}

WEATHER_CONDITIONS_FA = {
    "Sunny": "آفتابی", "Partly cloudy": "نیمه‌ابری", "Cloudy": "ابری",
    "Overcast": "کاملاً ابری", "Mist": "مه‌آلود", "Patchy rain possible": "احتمال بارش پراکنده",
    "Light rain": "باران سبک", "Moderate rain": "باران متوسط", "Heavy rain": "باران شدید",
    "Thunderstorm": "رعد و برق", "Thundery outbreaks possible": "احتمال رعد و برق"
}

history = []
last_location: Optional[str] = None
MAX_HISTORY = 5

def detect_time_hint(text: str) -> Optional[str]:
    for key, variants in TIME_KEYWORDS.items():
        if any(kw in text for kw in variants):
            return key
    return None

def extract_slots(text: str) -> Optional[WeatherQuery]:
    global last_location
    text = text.strip()
    norm_text = normalize_fa(text)
    location = None

    
    for fa_name_norm, en_name in CITY_TRANSLATIONS_NORM.items():
        if fa_name_norm in norm_text:
            location = en_name
            break

    
    if not location:
        match = re.search(r"در\s+(?P<city>[آ-ی]+)", norm_text)
        if match:
            possible_city = match.group("city")
            if possible_city in CITY_TRANSLATIONS_NORM:
                location = CITY_TRANSLATIONS_NORM[possible_city]

    
    if not location:
        words = re.findall(r"[آ-ی]+", norm_text)
        best_score = 0
        best_match = None
        for word in words:
            matches = difflib.get_close_matches(word, CITY_TRANSLATIONS_NORM.keys(), n=1, cutoff=0.75)
            if matches:
                m = matches[0]
                score = difflib.SequenceMatcher(None, word, m).ratio()
                if score > best_score:
                    best_score = score
                    best_match = m
        if best_match:
            location = CITY_TRANSLATIONS_NORM[best_match]

    # 4) fallback to last location
    if not location and last_location:
        location = last_location

    # time/data type detection (used downstream as hints)
    time_range = detect_time_hint(norm_text) or "today"

    data_type = "general"
    for key, variants in DATA_TYPE_KEYWORDS.items():
        if any(kw in norm_text for kw in variants):
            data_type = key
            break

    if not location:
        return None

    last_location = location
    return WeatherQuery(location=location, time_range=time_range, data_type=data_type)

def extract_requested_date(text: str) -> Optional[str]:
    today = datetime.date.today()
    weekday = today.weekday()
    norm_text = normalize_fa(text)

    # Named weekdays (e.g., "شنبه", with optional "هفته بعد/آینده")
    for fa_day, weekday_index in WEEKDAYS.items():
        if fa_day in norm_text:
            weeks_ahead = 0
            if "سه هفته بعد" in norm_text:
                weeks_ahead = 3
            elif "دو هفته بعد" in norm_text:
                weeks_ahead = 2
            elif "هفته بعد" in norm_text or "هفته آینده" in norm_text:
                weeks_ahead = 1
            days_ahead = (weekday_index - weekday + 7) % 7 + weeks_ahead * 7
            # If they asked the same day without "هفته بعد", assume today (0 days) is OK
            target_date = today + datetime.timedelta(days=days_ahead)
            return target_date.strftime("%Y-%m-%d")

    # Relative words
    if "امروز" in norm_text:
        return today.strftime("%Y-%m-%d")
    elif "فردا" in norm_text:
        return (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    elif "پس‌فردا" in norm_text or "پس فردا" in norm_text:
        return (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    # Words like "دو روز دیگر"
    for word, number in PERSIAN_NUMBER_WORDS.items():
        pattern = rf"{word}\s*روز\s*(دیگر|بعد)"
        if re.search(pattern, norm_text):
            target_date = today + datetime.timedelta(days=number)
            return target_date.strftime("%Y-%m-%d")

    # Numeric like "2 روز دیگر"
    match = re.search(r"(\d+)\s*روز\s*(دیگر|بعد)", norm_text)
    if match:
        days_later = int(match.group(1))
        target_date = today + datetime.timedelta(days=days_later)
        return target_date.strftime("%Y-%m-%d")

    return None

def build_weatherapi_url(query: WeatherQuery, api_key: str) -> str:
    q = urllib.parse.quote(query.location)
    return f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={q}&days=10&aqi=no&alerts=no"

def fetch_weather_data(url: str) -> Optional[dict]:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print("⚠️ خطای API:", data["error"].get("message"))
                return None
            return data
        else:
            print("⚠️ خطای API:", response.status_code)
    except Exception as e:
        print("❌ خطا در اتصال:", e)
    return None

def _safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        try:
            return int(float(x))
        except Exception:
            return default

def _fa_location_from_en(location_en: str) -> str:
    return next((fa for fa, en in CITY_TRANSLATIONS.items() if en == location_en), location_en)

def _format_current(query: WeatherQuery, data: dict) -> str:
    loc_fa = _fa_location_from_en(query.location)
    cur = data.get("current", {}) or {}
    cond_en = (cur.get("condition") or {}).get("text", "")
    cond_fa = WEATHER_CONDITIONS_FA.get(cond_en, cond_en)
    temp_c = cur.get("temp_c")
    humidity = cur.get("humidity")
    wind = cur.get("wind_kph")
    wind_desc = "نامشخص"
    if isinstance(wind, (int, float)):
        if wind < 15:
            wind_desc = "ملایم"
        elif wind < 30:
            wind_desc = "قابل توجه"
        else:
            wind_desc = "شدید"

    if query.data_type == "temperature":
        return f"🌡️ دمای الانِ {loc_fa}: {temp_c}°C"
    if query.data_type == "humidity":
        return f"💧 رطوبت الانِ {loc_fa}: {humidity}%"
    if query.data_type == "wind":
        return f"💨 سرعت باد الانِ {loc_fa}: {wind} km/h ({wind_desc})"
    if query.data_type == "rain":
        # Current endpoint doesn't guarantee rain chance; show condition instead
        return f"🌧️ وضعیت فعلی بارش در {loc_fa}: {cond_fa}"
    if query.data_type == "storm":
        return ("⚠️ احتمال طوفان" if ("storm" in cond_en.lower() or "thunder" in cond_en.lower())
                else "✅ طوفان گزارش نشده") + f" — وضعیت: {cond_fa}"

    return (
        f"⏱️ وضعیت الان در {loc_fa}:\n"
        f"🌡️ دما: {temp_c}°C\n"
        f"💧 رطوبت: {humidity}%\n"
        f"💨 باد: {wind} km/h ({wind_desc})\n"
        f"🔎 وضعیت: {cond_fa}"
    )

def _format_day_line(day: dict) -> str:
    d = day["date"]
    di = day["day"]
    cond = WEATHER_CONDITIONS_FA.get(di["condition"]["text"], di["condition"]["text"])
    rain = _safe_int(di.get("daily_chance_of_rain", 0), 0)
    return f"{d}: {cond} • {int(di['mintemp_c'])}–{int(di['maxtemp_c'])}°C • 💧 {rain}%"

def format_weather_response(query: WeatherQuery, data: dict, text: str) -> str:
    loc_fa = _fa_location_from_en(query.location)
    requested_date = extract_requested_date(text)
    time_hint = detect_time_hint(text) or query.time_range

    # Handle "now"
    if time_hint == "now":
        return _format_current(query, data)

    # Guard forecast presence
    forecast_list = (data.get("forecast") or {}).get("forecastday") or []
    if not forecast_list:
        return "❌ داده‌ای از پیش‌بینی موجود نیست."

    # If no explicit date found, pick based on hint
    if not requested_date:
        if time_hint == "tomorrow" and len(forecast_list) >= 2:
            requested_date = forecast_list[1]["date"]
        elif time_hint == "today" or time_hint is None:
            requested_date = forecast_list[0]["date"]
        elif time_hint == "week":
            # Return a brief 7-day overview
            lines = ["🗓️ پیش‌بینی ۷ روز آینده:"]
            for day in forecast_list[:7]:
                lines.append(_format_day_line(day))
            return "\n".join(lines)

    # Find that day
    forecast_day = None
    chosen_date = ""
    for day in forecast_list:
        if day["date"] == requested_date:
            forecast_day = day["day"]
            chosen_date = day["date"]
            break

    if not forecast_day:
        return "🔎 اطلاعاتی برای تاریخ موردنظر یافت نشد."

    max_temp = forecast_day["maxtemp_c"]
    min_temp = forecast_day["mintemp_c"]
    humidity = forecast_day.get("avghumidity")
    wind = forecast_day.get("maxwind_kph")
    cond_en = (forecast_day.get("condition") or {}).get("text", "")
    cond_fa = WEATHER_CONDITIONS_FA.get(cond_en, cond_en)
    rain_chance = _safe_int(forecast_day.get("daily_chance_of_rain", 0), 0)

    # Specific data-type responses
    if query.data_type == "rain":
        if rain_chance > 50:
            return f"✅ بله، در روز {chosen_date} در {loc_fa} احتمال بارندگی وجود دارد ({rain_chance}%). 🌂"
        else:
            return f"❌ خیر، بارندگی در روز {chosen_date} در {loc_fa} پیش‌بینی نشده است ({rain_chance}%)."

    if query.data_type == "storm":
        is_stormy = ("storm" in cond_en.lower()) or ("thunder" in cond_en.lower()) or (isinstance(wind, (int, float)) and wind > 40)
        return f"{'⚠️ بله،' if is_stormy else '✅ خیر،'} وضعیت طوفانی برای {loc_fa} در روز {chosen_date} {'پیش‌بینی شده' if is_stormy else 'گزارش نشده'} است."

    if query.data_type == "temperature":
        return f"🌡️ دمای {loc_fa} در روز {chosen_date}: {min_temp}°C تا {max_temp}°C"

    if query.data_type == "humidity":
        return f"💧 رطوبت در {loc_fa} در روز {chosen_date}: {humidity}%"

    if query.data_type == "wind":
        wind_desc = "نامشخص"
        if isinstance(wind, (int, float)):
            if wind < 15:
                wind_desc = "ملایم"
            elif wind < 30:
                wind_desc = "قابل توجه"
            else:
                wind_desc = "شدید"
        return f"💨 سرعت باد در {loc_fa} در روز {chosen_date}: {wind} km/h ({wind_desc})"

    # General daily summary
    return (
        f"📅 پیش‌بینی برای {chosen_date} در {loc_fa}:\n"
        f"🌡️ دما: {min_temp}°C تا {max_temp}°C\n"
        f"💧 رطوبت: {humidity}%\n"
        f"💨 باد: {wind} km/h\n"
        f"🌧️ احتمال بارندگی: {rain_chance}%\n"
        f"🔎 وضعیت: {cond_fa}"
    )

def run_gui_weather_bot():
    def on_submit():
        user_input = entry.get()
        query = extract_slots(user_input)
        if not query:
            result_var.set("❌ شهر معتبری پیدا نشد.")
            return

        api_key = "df54ad656a59426b8b050734252808"  # ← put your valid WeatherAPI key
        url = build_weatherapi_url(query, api_key)
        data = fetch_weather_data(url)
        if data:
            result = format_weather_response(query, data, user_input)
            result_var.set(result)
            entry.delete(0, tk.END)

            history.append((user_input, result))
            if len(history) > MAX_HISTORY:
                history.pop(0)

            history_text.configure(state="normal")
            history_text.delete(1.0, tk.END)
            for q, a in history:
                history_text.insert(tk.END, f"❓ {q}\n✅ {a}\n\n")
            history_text.configure(state="disabled")
        else:
            result_var.set("❌ دریافت اطلاعات آب‌وهوا با مشکل مواجه شد.")

    root = tk.Tk()
    root.title("دستیار آب‌وهوا ☁️")
    root.geometry("600x550")
    root.configure(bg="#e9f5ff")

    frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
    frame.pack(expand=True, fill="both", padx=15, pady=15)

    label = tk.Label(frame, text="❓ سوال خود را درباره‌ی هوا بپرس:", font=("Vazirmatn", 14), bg="#ffffff", anchor="w")
    label.pack(pady=(0, 5), fill="x")

    entry = tk.Entry(frame, font=("Vazirmatn", 13), justify="right", width=50)
    entry.pack(pady=(0, 10))

    submit_button = tk.Button(frame, text="🔍 بررسی کن", font=("Vazirmatn", 12, "bold"), command=on_submit)
    submit_button.pack(pady=(0, 15))

    result_var = tk.StringVar()
    result_label = tk.Label(frame, textvariable=result_var, font=("Vazirmatn", 13), bg="#ffffff", justify="right", wraplength=500)
    result_label.pack()

    global history_text
    history_label = tk.Label(frame, text="🕘 تاریخچه‌ی گفتگو:", font=("Vazirmatn", 12, "bold"), bg="#ffffff", anchor="w")
    history_label.pack(pady=(10, 0), fill="x")

    history_text = tk.Text(frame, font=("Vazirmatn", 11), bg="#f5f5f5", height=8, wrap="word", state="disabled")
    history_text.pack(fill="both", expand=False)

    root.mainloop()

if __name__ == "__main__":
    run_gui_weather_bot()
