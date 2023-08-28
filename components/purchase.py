from dataclasses import dataclass
import time

from localization.localization import localize


@dataclass
class Purchase:
    name: str
    price_for_one: float
    quantity: int = 1
    customer: str = "Anonymous"
    purchase_date: str = time.strftime("%d/%m/%Y %H:%M:%S")

    def get_item_info(self, language="en") -> str:
        """
        Returns info about item
        :return: str
        """
        return f"{self.name}\n" \
                f"{localize(language, 'price_for_one')}: {self.price_for_one}\n" \
                f"{localize(language, 'quantity')}: {self.quantity}\n" \
                f"{localize(language, 'customer')}: {self.customer}\n" \
                f"{localize(language, 'date')}: {self.purchase_date}\n"

