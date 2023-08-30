from dataclasses import dataclass

from localization.localization import localize


@dataclass
class Purchase:
    name: str
    price_for_one: float
    quantity: int = 1

    def get_item_info(self, language="en") -> str:
        """
        Returns info about item
        :return: str
        """
        return f"{localize(language, 'name')}: \"{self.name}\"\n" \
                f"{localize(language, 'price_for_one')}: {self.price_for_one}\n" \
                f"{localize(language, 'quantity')}: {self.quantity}\n"

