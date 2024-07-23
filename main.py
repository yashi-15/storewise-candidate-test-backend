import traceback
from doctest import UnexpectedException
from typing import List
import inquirer 
#I have used inquirer library instead of "bullet" because I was not able to use bullet in Windows, inquirer has the same functionality as bullet. RUN BELOW COMMAND BEFORE RUNNING THE CODE:
# pip install inquirer


class PurchaseItem(object):
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)


def get_total_order_amount(order: List[PurchaseItem]):

    """
    The total cost of all the items ordered
    """

    return sum(item.price for item in order)
    


def get_service_charge(order: List[PurchaseItem]):

    """
    For every Rs. 100, the service charge amount should increase by 1% of order amount, upto a max of 20%
    Eg:
        Order Amount = 80, Service Charge = 0
        Order Amount = 150, Service Charge = 1.5
        Order Amount = 800, Service Charge = 64
        Order Amount = 1500, Service Charge = 225
        Order Amount = 3000, Service Charge = 600
    """

    total_amount = get_total_order_amount(order)
    if total_amount < 100:
        return 0
    service_charge = 0.01 * (total_amount // 100) * total_amount
    return min(service_charge, 0.20 * total_amount)


class Option(object):
    def __init__(self, n=None, pu=None, p=None, d=None):
        self.p = p
        self.n = n
        self.pu = pu
        if d:
            self.n = d.get("name")
            self.p = d.get("price")
        if self.p == None:
            self.p = 0
        if self.n == None:
            raise AttributeError
        self.pu = self.pu if self.pu else "Rs."

    def __str__(self):
        return f"{str(self.n)} {str(self.pu) + ' ' + str(self.p) if self.p else ''}"

    def __len__(self):
        return len(self.__str__())


MCDONALDS_FOOD_OPTIONS = [
    Option(d={"name": "Veg Burger", "price": 115.00}),
    Option(d={"name": "Veg Wrap", "price": 130.00}),
    Option(d={"name": "Veg Happy Meal", "price": 215.00}),
    Option(d={"name": "Chicken Burger", "price": 175.00}),
    Option(d={"name": "Chicken Wrap", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option(d={"name": "Sprite (M)", "price": 115.00}),
    Option(d={"name": "Sprite (L)", "price": 130.00}),
    Option(d={"name": "Mango Smoothie", "price": 215.00}),
    Option(d={"name": "Chocolate Smoothie", "price": 175.00}),
    Option(d={"name": "Chocolate Smoothie w/ Icecream", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]


def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option

    raise UnexpectedException


def print_order(order):
    print()

    try:
        total_amount = get_total_order_amount(order)
    except:
        traceback.print_exc()
        total_amount = "ERROR"

    service_charge = "ERROR"
    if total_amount != "ERROR":
        try:
            service_charge = get_service_charge(order)
        except:
            traceback.print_exc()
            service_charge = "ERROR"

    print("Final Order")
    for i, item in enumerate(order):
        print(f"{i+1}. {item.name}")

    print(f"Order Amount: {str(total_amount)}")
    print(f"Service Charge: {str(service_charge)}")
    print(f"Final Amount: {str(total_amount + service_charge) if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float)) else 'ERROR'}")


print()
print("Welcome to McDonalds on your shell :)")
print("Here you can place your order")
print("And then we will show you your bill")
print()
order = []
while True:
    options = list(map(lambda x: str(x), MCDONALDS_FOOD_OPTIONS))
    question = [inquirer.List('option', message="Add an item", choices=options)]
    result = inquirer.prompt(question)['option']
    option = get_option_from_result(result, MCDONALDS_FOOD_OPTIONS)
    if result == str(MCDONALDS_FOOD_OPTIONS[-1]):
        break
    order.append(PurchaseItem(option))
    print(f"{result} is added to your order")

while True:
    options = list(map(lambda x: str(x), MCDONALDS_BEVERAGES_OPTIONS))
    question = [inquirer.List('option', message="Add a beverage", choices=options)]
    result = inquirer.prompt(question)['option']
    option = get_option_from_result(result, MCDONALDS_BEVERAGES_OPTIONS)
    if result == str(MCDONALDS_BEVERAGES_OPTIONS[-1]):
        break
    order.append(PurchaseItem(option))
    print(f"{result} is added to your order")

print()
print_order(order)
