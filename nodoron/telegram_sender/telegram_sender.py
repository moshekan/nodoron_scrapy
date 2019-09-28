from typing import List

from nodoron.db import get_session, Apartment, SearchRequest, SentApartment, RequestLocation
from nodoron.utils.telegram_bot import send_new_apartment_message


def is_apartment_in_any_of_request_locations(apartment, request_locations: List[RequestLocation]):
    return any(request_location.is_apartment_within_range(apartment) for request_location in request_locations)


class TelegramSender(object):

    def __init__(self, search_request: SearchRequest):
        self.search_request = search_request
        self.session = get_session()


    def get_new_apartments_for_search_request(self) -> List[Apartment]:
        apartments = (self.session.query(Apartment)
                 .filter_by(city=self.search_request.city)
                 .filter(Apartment.price >= self.search_request.min_price)
                 .filter(Apartment.price <= self.search_request.max_price)).all()

        previous_apartment_ids = [sent_apartment.apartment_id for sent_apartment in self.search_request.sent_apartments]
        new_apartments = [apartment for apartment in apartments if apartment.id not in previous_apartment_ids]

        return [new_apartment for new_apartment in new_apartments
                                   if is_apartment_in_any_of_request_locations(new_apartment,
                                                                               self.search_request.locations)]


    def send_messages_for_new_apartments_for_search_request(self):
        new_apartments = self.get_new_apartments_for_search_request()
        for new_apartment in new_apartments:
            sent_apartment = SentApartment()
            self.session.add(sent_apartment)
            sent_apartment.apartment = new_apartment
            sent_apartment.search_request = self.search_request
            send_new_apartment_message(apartment=new_apartment,
                                       chat_id=self.search_request.chat_id,
                                       phone_number_list=[])
            self.session.commit()


def send_for_all_search_requests():
    session = get_session()
    for search_request in session.query(SearchRequest).all():
        TelegramSender(search_request).send_messages_for_new_apartments_for_search_request()
