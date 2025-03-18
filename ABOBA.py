from abc import ABC, abstractmethod
from math import sqrt

# Исключение для недостаточного баланса
class InsufficientBalanceException(Exception):
    def __init__(self, required, available):
        self.required = required
        self.available = available
        super().__init__(f"Недостаточно средств. Требуется: {required}, доступно: {available}")

# Исключение для недопустимого возраста
class InvalidAgeException(Exception):
    def __init__(self, age, min_age, max_age):
        self.age = age
        self.min_age = min_age
        self.max_age = max_age
        super().__init__(f"Недопустимый возраст: {age}. Допустимый диапазон: {min_age}-{max_age}")

# Абстрактный класс для товаров
class Product(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @abstractmethod
    def get_details(self):
        pass

# Класс для книг
class Book(Product):
    def __init__(self, name, price, author):
        super().__init__(name, price)
        self._author = author

    def get_details(self):
        return f"Книга: {self.name}, Автор: {self._author}, Цена: {self.price}"

# Класс для электроники
class Electronic(Product):
    def __init__(self, name, price, brand):
        super().__init__(name, price)
        self._brand = brand

    def get_details(self):
        return f"Электроника: {self.name}, Бренд: {self._brand}, Цена: {self.price}"

# Класс для управления корзиной покупок
class ShoppingCart:
    def __init__(self):
        self._items = []

    def add_item(self, product):
        self._items.append(product)

    def remove_item(self, product):
        if product in self._items:
            self._items.remove(product)

    def get_total_price(self):
        return sum(item.price for item in self._items)

    def clear_cart(self):
        self._items.clear()

    def get_items(self):
        return self._items

# Класс для управления историей покупок
class PurchaseHistory:
    def __init__(self):
        self._purchases = []

    def add_purchase(self, items):
        self._purchases.extend(items)

    def get_purchases(self):
        return self._purchases

# Класс для управления счетом пользователя
class Account:
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            return True
        raise InsufficientBalanceException(amount, self._balance)
        return False

    @property
    def balance(self):
        return self._balance

# Функция для отображения главного меню
def display_menu():
    print("Добро пожаловать. Выберите действие:")
    print("1) Посмотреть категории")
    print("2) Перейти в корзину")
    print("3) Перейти в историю покупок")
    print("4) Посмотреть счет")
    print("5) Выйти")

# Функция для отображения категорий товаров
def display_categories(categories):
    print("Выберите категорию:")
    for i, category in enumerate(categories.keys(), start=1):
        print(f"{i}) {category}")

# Функция для отображения товаров в выбранной категории
def display_products(products):
    print("Выберите товар:")
    for i, product in enumerate(products, start=1):
        print(f"{i}) {product.get_details()}")

# Главная функция программы
def main():
    categories = {
        "Книги": [
            Book("1984", 500, "Джордж Оруэлл"),
            Book("Мастер и Маргарита", 600, "Михаил Булгаков")
        ],
        "Электроника": [
            Electronic("iPhone 13", 60000, "Apple"),
            Electronic("Samsung Galaxy S21", 55000, "Samsung")
        ]
    }

    shopping_cart = ShoppingCart()
    purchase_history = PurchaseHistory()
    account = Account(10000)

    while True:
        display_menu()
        choice = input("Введите номер действия: ")

        if choice == '1':
            display_categories(categories)
            try:
                category_choice = int(input("Введите номер категории: "))
                selected_category = list(categories.keys())[category_choice - 1]
                display_products(categories[selected_category])
                product_choice = int(input("Введите номер товара: "))
                selected_product = categories[selected_category][product_choice - 1]
                shopping_cart.add_item(selected_product)
                print(f"Товар '{selected_product.name}' добавлен в корзину.")
            except (ValueError, IndexError):
                print("Неверный выбор. Попробуйте снова.")

        elif choice == '2':
            cart_items = shopping_cart.get_items()
            if not cart_items:
                print("Корзина пуста.")
            else:
                print("Ваша корзина:")
                for item in cart_items:
                    print(item.get_details())
                print(f"Общая стоимость: {shopping_cart.get_total_price()}")
                buy_choice = input("Хотите оформить покупку? (да/нет): ")
                if buy_choice.lower() == 'да':
                    try:
                        account.withdraw(shopping_cart.get_total_price())
                        purchase_history.add_purchase(cart_items)
                        shopping_cart.clear_cart()
                        print("Покупка оформлена успешно!")
                    except InsufficientBalanceException as e:
                        print(e)

        elif choice == '3':
            purchases = purchase_history.get_purchases()
            if not purchases:
                print("История покупок пуста.")
            else:
                print("История покупок:")
                for item in purchases:
                    print(item.get_details())

        elif choice == '4':
            print(f"Ваш баланс: {account.balance}")
            deposit_choice = input("Хотите пополнить счет? (да/нет): ")
            if deposit_choice.lower() == 'да':
                try:
                    deposit_amount = float(input("Введите сумму для пополнения: "))
                    account.deposit(deposit_amount)
                    print(f"Счет пополнен на {deposit_amount}. Новый баланс: {account.balance}")
                except ValueError:
                    print("Неверная сумма. Попробуйте снова.")

        elif choice == '5':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()