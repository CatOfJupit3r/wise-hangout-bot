from dataclasses import dataclass
import time
import json

@dataclass
class Purchase:
    name: str
    price_for_one: float
    quantity: int = 1
    customer: str = "Anonymous"
    purchase_date: str = time.strftime("%d/%m/%Y %H:%M:%S")
