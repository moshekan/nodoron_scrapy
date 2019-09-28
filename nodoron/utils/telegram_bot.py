# -*- coding: utf-8 -*-
from typing import List

from requests import get
import os


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


def send_message(message: str, chat_id: str):
    url = TELEGRAM_API_URL.format(token=BOT_TOKEN, chat_id=chat_id, text=message)
    get(url).raise_for_status()


def send_new_apartment_message(apartment, chat_id: str, phone_number_list: List[str]):
    whatsapp_link = '\n'.join([WHATSAPP_LINK_URL.format(
        number=number,
        text=WHATSAPP_TEXT_FORMAT.format(address=apartment.street, url=apartment.view_url)
    ) for number in phone_number_list])

    message = APARTMENT_MESSAGE.format(
        rooms=apartment.rooms,
        size=apartment.square_meters,
        latitude=apartment.coordinates_latitude,
        longitude=apartment.coordinates_longitude,
        neighborhood=apartment.neighborhood,
        title=apartment.title,
        price=apartment.price,
        merchant='עם תיווך' if apartment.merchant else 'ללא תיווך',
        date_added=apartment.date_added,
        view_url=apartment.view_url,
        id=apartment.yad2_id,
        whatsapp_link=whatsapp_link
    )
    send_message(message, chat_id)
