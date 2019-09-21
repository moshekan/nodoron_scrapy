from requests import get
import datetime
import pytz
import os
import urllib.parse


BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_BOT_CHAT_ID')

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=HTML&disable_web_page_preview'

WHATSAPP_TEXT_FORMAT = """
היי, לגבי הדירה ברחוב {address}, {url} , עוד רלוונטי?"""
WHATSAPP_LINK_URL = '<a href="https://wa.me/972{number}/?text={text}">{number}</a>'


APARTMENT_MESSAGE = """
<strong>מצאתי דירה חדשה</strong>
דירת {rooms} חדרים בגודל {size} מ״ר
<a href="https%3A%2F%2Fwww.google.com%2Fmaps%2Fsearch%2F%3Fapi%3D1%26query%3D{latitude},{longitude}">{title}, {neighborhood}</a>
שכר דירה {price} ₪
תיווך: {merchant}
נוספה בתאריך: {date_added}
{view_url}
{whatsapp_link}
<i>ID: {id}</i>
"""

STARTING_SEARCH_MESSAGE = """
מתחיל את החיפוש של השעה {time}
"""

ERROR_MESSAGE = """
<strong>חטפתי שגיאה</strong>
{message}
"""

def send_message(message):
    url = TELEGRAM_API_URL.format(token=BOT_TOKEN, chat_id=CHAT_ID, text=message)
    response = get(url)


def send_new_apartment_message(item, phone_number_list):
    whatsapp_link = '\n'.join([WHATSAPP_LINK_URL.format(
        number=number,
        text=WHATSAPP_TEXT_FORMAT.format(address=item['street'], url=item['view_url'])
    ) for number in phone_number_list])

    message = APARTMENT_MESSAGE.format(
        rooms=item.get('rooms'),
        size=item.get('square_meters'),
        latitude=item.get('coordinates_latitude'),
        longitude=item.get('coordinates_longitude'),
        neighborhood=item.get('neighborhood'),
        title=item.get('title'),
        price=item.get('price'),
        merchant='עם תיווך' if item.get('merchant') else 'ללא תיווך',
        date_added=item.get('date_added'),
        view_url=item.get('view_url'),
        id=item.get('id'),
        whatsapp_link=whatsapp_link
    )
    send_message(message)


def send_starting_search_message():
    send_message(STARTING_SEARCH_MESSAGE.format(time=datetime.datetime.now(tz=pytz.timezone('Asia/Jerusalem')).strftime("%H:%M")))


def send_error_message(message):
    send_message(ERROR_MESSAGE.format(message=message))
