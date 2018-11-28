from random import randint
from typing import Any, Callable, Dict, List, Union
from uuid import uuid4

from loading.domain import AccountId, Event, EventType


def _get_random(items: List[Any]) -> Any:
    """ Return random account from list of items """
    return items[randint(0, len(items) - 1)]


def random_account(account_ids: List[AccountId]) -> AccountId:
    """ Return a random account from list of accounts """
    return _get_random(account_ids)


def random_email(emails: List[str]) -> str:
    """ Return a random email from a list of emails """
    return _get_random(emails)


def random_email_or_nothing(
    emails: List[str],
    weighting: int
) -> Union[str, None]:
    """
    Generate either a random email or nothing.  Randomly chooses a number
    between 1-100 if that number is > weight, return None, else a random email.
    """
    choice = randint(1, 100)
    if choice > weighting:
        return None
    else:
        return random_email(emails)


def event_key():
    """ Return a guid for an event key """
    return uuid4().hex


def random_url(urls: List[str]) -> str:
    """ Return a random url """
    return _get_random(urls)


def random_event_type() -> EventType:
    return _get_random(list(EventType.__members__.values())).value


def random_conversion_id(ids: List[int]) -> int:
    """ Return a random conversion id """
    return _get_random(ids)


def generate_account_ids(count: int = 1) -> List[AccountId]:
    return [randint(10000, 20000) for _i in range(1, count)]


def generate_emails(count: int = 1, domain: str = "example.com"):
    return [f'user{i}@{domain}' for i in range(1, count)]


def generate_account_event_keys(
    account_ids: List[AccountId]
) -> Dict[AccountId, str]:
    return {id: event_key() for id in account_ids}


def generate_event_data():
    return dict(id=uuid4().hex)


def generate_visit_data(email: str) -> Dict[str, str]:
    return dict(email=email)


def generate_event_fn(
    account_ids: List[AccountId],
    emails: List[str]
) -> Callable[[], Event]:
    event_keys = generate_account_event_keys(account_ids)

    def generate_event():
        account_id = random_account(account_ids)
        email = random_email(emails)
        return Event(
            account_id,
            event_keys[account_id],
            random_event_type(),
            generate_event_data(),
            generate_visit_data(email)
        )
    return generate_event
