import traceback
from doctest import UnexpectedException
from typing import List
import inquirer
#I have used inquirer library instead of "bullet" because I was not able to use bullet in Windows, inquirer has the same functionality as bullet. RUN BELOW COMMAND BEFORE RUNNING THE CODE:
# pip install inquirer

class PurchaseItem:
    def __init__(self, option):
        self.price = option.price
        self.name = str(option)

class Option:
    def __init__(self, name, price, unit="Rs."):
        self.name = name
        self.price = price
        self.unit = unit

    def __str__(self):
        return f"{self.name} {self.unit} {self.price}"

    def __len__(self):
        return len(str(self))

def get_total_order_amount(order: List[PurchaseItem]):
    return sum(item.price for item in order)
    
def get_service_charge(order: List[PurchaseItem]):
    total_amount = get_total_order_amount(order)
    if total_amount < 100:
        return 0
    service_charge = 0.01 * (total_amount // 100) * total_amount
    return min(service_charge, 0.20 * total_amount)

def print_order(order):
    try:
        total_amount = get_total_order_amount(order)
    except:
        traceback.print_exc()
        total_amount = "ERROR"

    try:
        service_charge = get_service_charge(order)
    except:
        traceback.print_exc()
        service_charge = "ERROR"

    print("Final Order")
    for i, item in enumerate(order):
        print(f"{i+1}. {item.name}")

    print(f"Order Amount: {total_amount}")
    print(f"Service Charge: {service_charge}")
    print(f"Final Amount: {total_amount + service_charge if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float)) else 'ERROR'}")

def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option
    raise UnexpectedException

MCDONALDS_FOOD_OPTIONS = [
    Option("Veg Burger", 115.00),
    Option("Veg Wrap", 130.00),
    Option("Veg Happy Meal", 215.00),
    Option("Chicken Burger", 175.00),
    Option("Chicken Wrap", 195.00),
    Option("No, that's all", 0.00),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option("Sprite (M)", 115.00),
    Option("Sprite (L)", 130.00),
    Option("Mango Smoothie", 215.00),
    Option("Chocolate Smoothie", 175.00),
    Option("Chocolate Smoothie w/ Icecream", 195.00),
    Option("No, that's all", 0.00),
]

def main():
    print("Welcome to McDonalds on your shell :)")
    print("Here you can place your order")
    print("And then we will show you your bill")
    print()

    order = []
    while True:
        options = [str(option) for option in MCDONALDS_FOOD_OPTIONS]
        question = [inquirer.List('option', message="Add an item", choices=options)]
        result = inquirer.prompt(question)['option']
        option = get_option_from_result(result, MCDONALDS_FOOD_OPTIONS)
        if result == str(MCDONALDS_FOOD_OPTIONS[-1]):
            break
        order.append(PurchaseItem(option))
        print(f"{result} is added to your order")

    while True:
        options = [str(option) for option in MCDONALDS_BEVERAGES_OPTIONS]
        question = [inquirer.List('option', message="Add a beverage", choices=options)]
        result = inquirer.prompt(question)['option']
        option = get_option_from_result(result, MCDONALDS_BEVERAGES_OPTIONS)
        if result == str(MCDONALDS_BEVERAGES_OPTIONS[-1]):
            break
        order.append(PurchaseItem(option))
        print(f"{result} is added to your order")

    print()
    print_order(order)

if __name__ == "__main__":
    main()