import os
import re
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

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STOPWORDS_PATH = os.path.join(BASE_PATH, "data", "stopWords.txt")

with open(STOPWORDS_PATH, "r", encoding="utf-8") as f:
    STOPWORDS = [line.strip() for line in f.readlines() if line.strip()]




INTENT_KEYWORDS = {
    "مکان و کشور": [
        "پایتخت", "مرکز", "کجاست", "مساحت", "در کجا", "واقع شده", "نقشه",  "شهر", "کشور", "استان",
        "شهرستان", "ایالت", "پارک", "باغ‌وحش", "موزه",  "کوه", "کوهستان", "فلات", "دریا", "جنگل", "جلگه"
    ],
    "اطلاعات افراد": [
        "کی بود", "چه کسی بود", "کشفیات", "اختراعات", "اختراع", "کاشف", "متولد", "درگذشت", "آثار",
        "زندگی نامه", "بیوگرافی", "کیه"
    ],
    "تاریخی": [
        "چه سالی", "چه زمانی", "چه تاریخی", "در چه سالی", "قرن", "قرون", "تمدن",
        "سلسله", "آثار باستانی", "باستان", "شاه", "سلطنت", "امپراطوری", "حزب", "جنبش", "کودتا", "قیام"
    ],
    "تعاریف": [
        "چیست", "یعنی", "یعنی چه", "چی", "به چه معناست", "معنی", "تعریف"
    ],
    "تکنولوژی": [
        "هوش مصنوعی", "اینترنت", "علم", "دانش", "ابزار", "سیستم عامل","برنامه نویسی", "کامپیوتر",
        "لپ تاپ", "هوشمند", "دیجیتال"
    ]
}


INTENT_TO_DATA_TYPE = {
    "مکان و کشور": "جغرافیایی",
    "اطلاعات افراد": "بیوگرافی",
    "تاریخی": "تاریخی",
    "تعاریف": "علمی",
    "تکنولوژی": "علمی"
}

def detect_intent(question: str) -> Optional[str]:
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in question:
                return intent
    return None

def extract_main_concept(question: str, intent: Optional[str]) -> str:
    if intent:
        for kw in INTENT_KEYWORDS[intent]:
            question = re.sub(re.escape(kw), "", question, flags=re.IGNORECASE)
    tokens = question.split()
    filtered_tokens = [
        word for word in tokens
        if word not in STOPWORDS
    ]
    concept = " ".join(filtered_tokens)
    concept = re.sub(r"[؟?!\.،]", "", concept).strip()
    concept = re.sub(r"\s+", " ", concept)
    return concept

def analyze_question(question: str) -> Dict[str, Optional[str]]:
    intent = detect_intent(question)
    concept = extract_main_concept(question, intent)
    data_type = INTENT_TO_DATA_TYPE.get(intent, "نامشخص")
    return {
        "intent": intent,
        "main_concept": concept,
        "data_type": data_type
    }


def run(command, iom, profile, map):
    try:
        result = analyze_question(command)
        output = f"دسته: {result['data_type']}، مفهوم: {result['main_concept']}"
        print(output)
        iom.getSpeaker().say(output)
    except Exception as e:
        print("خطا در اجرای تحلیل سوال:", e)
        iom.getSpeaker().say("مشکلی در تحلیل سوال پیش آمد.")