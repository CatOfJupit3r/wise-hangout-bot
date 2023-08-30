from dataclasses import dataclass

import settings
from localization.localization import localize


@dataclass
class Purchase:
    name: str
    price_for_one: float
    quantity: int = 1

    def get_item_info(self, user_id=settings.OWNER_ID) -> str:
        """
        Returns info about item
        :return: str
        """
        return f"{localize(user_id, 'name')}: \"{self.name}\"\n" \
                f"{localize(user_id, 'price_for_one')}: {self.price_for_one}\n" \
                f"{localize(user_id, 'quantity')}: {self.quantity}\n"

