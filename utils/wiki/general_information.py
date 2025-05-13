import os
import re
import wikipedia
import webbrowser
from typing import Optional, Dict

KEYWORDS = [
    "پایتخت", "مرکز", "کجاست", "مساحت", "در کجا", "واقع شده", "نقشه",
    "شهر", "کشور", "استان", "شهرستان", "ایالت", "پارک", "باغ‌وحش", "موزه",
    "کوه", "کوهستان", "فلات", "دریا", "جنگل", "جلگه",
    "کی بود", "چه کسی بود", "کشفیات", "اختراعات", "اختراع", "کاشف",
    "متولد", "درگذشت", "آثار", "زندگی نامه", "بیوگرافی", "کیه",
    "چه سالی", "چه زمانی", "چه تاریخی", "در چه سالی", "قرن", "قرون",
    "تمدن", "سلسله", "آثار باستانی", "باستان", "شاه", "سلطنت",
    "امپراطوری", "حزب", "جنبش", "کودتا", "قیام",
    "چیست", "یعنی", "یعنی چه", "چی", "به چه معناست", "معنی", "تعریف",
    "هوش مصنوعی", "اینترنت", "علم", "دانش", "ابزار", "سیستم عامل",
    "برنامه نویسی", "کامپیوتر", "لپ تاپ", "هوشمند", "دیجیتال"
]

PRIORITY = 10

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STOPWORDS_FILE = os.path.join(BASE, "data", "stopWords.txt")
with open(STOPWORDS_FILE, encoding="utf-8") as f:
    STOPWORDS = {w.strip() for w in f if w.strip()}

INTENT_KEYWORDS = {
    "مکان و کشور": ["پایتخت", "مرکز", "کجاست", "مساحت", "در کجا", "واقع شده", "نقشه",  "شهر", "کشور", "استان",
        "شهرستان", "ایالت", "پارک", "باغ‌وحش", "موزه",  "کوه", "کوهستان", "فلات", "دریا", "جنگل", "جلگه"],

    "اطلاعات افراد": ["کی بود", "چه کسی بود", "کشفیات", "اختراعات", "اختراع", "کاشف", "متولد", "درگذشت", "آثار",
    "زندگی نامه", "بیوگرافی", "کیه"],

    "تاریخی": ["چه سالی", "چه زمانی", "چه تاریخی", "در چه سالی", "قرن", "قرون", "تمدن",
    "سلسله", "آثار باستانی", "باستان", "شاه", "سلطنت", "امپراطوری", "حزب", "جنبش", "کودتا", "قیام"],

    "تعاریف": ["چیست", "یعنی", "یعنی چه", "چی", "به چه معناست", "معنی", "تعریف"],

    "تکنولوژی": ["هوش مصنوعی", "اینترنت", "علم", "دانش", "ابزار", "سیستم عامل","برنامه نویسی", "کامپیوتر",
      "لپ تاپ", "هوشمند", "دیجیتال"]
}


INTENT_TO_DATA_TYPE = {
    "مکان و کشور": "جغرافیایی",
    "اطلاعات افراد": "بیوگرافی",
    "تاریخی": "تاریخی",
    "تعاریف": "علمی",
    "تکنولوژی": "علمی"
}

def detect_intent(text: str) -> Optional[str]:
    for intent, kws in INTENT_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                return intent
    return None

def extract_concept(text: str, intent: Optional[str]) -> str:
    if intent:
        for kw in INTENT_KEYWORDS[intent]:
            text = re.sub(re.escape(kw), "", text, flags=re.IGNORECASE)
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]
    concept = " ".join(words)
    return re.sub(r"[؟?!،\.]", "", concept).strip()

def analyze_question(text: str) -> Dict[str, Optional[str]]:
    intent = detect_intent(text)
    concept = extract_concept(text, intent) if intent else ""
    dtype = INTENT_TO_DATA_TYPE.get(intent, "نامشخص")
    return {"intent": intent, "main_concept": concept, "data_type": dtype}


def wiki_lookup(query: str, lang: str = "fa") -> Dict[str, str]:
    try:
        wikipedia.set_lang(lang)
        results = wikipedia.search(query, 5)
        if not results:
            return {"summary": "موردی پیدا نشد.", "url": ""}
        page = wikipedia.page(results[0], auto_suggest=True)
        summary = page.summary.split("\n")[0]
        summary = re.sub(r"[^)]*", "", summary)
        return {"summary": summary.strip(), "url": page.url}
    except Exception as e:
        return {"summary": f"خطا در ویکی‌پدیا: {e}", "url": ""}


def run(command, iom, profile, mapper):
    res = analyze_question(command)
    intent = res["intent"]; concept = res["main_concept"]; dtype = res["data_type"]
    if not intent:
        print("متأسفم، متوجه نوع سؤال نشدم.")
        return
    print(f"[Info] سؤال در حوزهٔ {dtype} است. در حال جست‌وجو ...")
    data = wiki_lookup(concept)
    print(["summary"] , data["summary"])
    print("→", data["summary"])
    if data["url"]:
        print("برای مطالعه بیشتر:", data["url"])
        webbrowser.open(data["url"])