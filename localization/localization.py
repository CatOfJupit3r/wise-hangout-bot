import json
from functools import lru_cache

import settings


def add_user_to_database(user_id: int | str, chosen_language: str) -> None:
    """
    Adds user to database
    :param user_id: id of user. If value is integer, it will be converted to string
    :param username: username of user
    :return: None
    """
    if isinstance(user_id, int):
        user_id = str(user_id)
    with open("database/users.json", "r+") as f:
        localization = json.load(f)
    localization[user_id]["language"] = chosen_language
    with open("database/users.json", "w+") as f:
        json.dump(localization, f, indent=4)


def get_user_language(user_id: int | str) -> str:
    """
    Returns user language
    :param user_id: id of user. If value is integer, it will be converted to string
    :return: str
    """
    if isinstance(user_id, int):
        user_id = str(user_id)
    with open("database/users.json", "r+") as f:
        localization = json.load(f)
    return localization[user_id]["language"]


def localize(user_id: int | str, text: str) -> str:
    """
    Returns localized text
    :param user_id: id of user. If value is integer, it will be converted to string
    :param text: text to localize
    :return: str
    """
    if isinstance(user_id, int):
        user_id = str(user_id)
    user_language = get_user_language(user_id)
    return __retrieve_phrase(user_language, text)


@lru_cache()
def __retrieve_phrase(language: str, identifier: str) -> str:
    """
    Returns localized phrase
    :param language: language to localize
    :param identifier: phrase identifier
    :return: str
    """
    with open(f"localization/{language}.json", "r+") as f:
        phrases = json.load(f)
    if identifier not in phrases:
        settings.logger_errors.error(f"Phrase {identifier} not found in {language}.json")
        return identifier
    return phrases[identifier]

