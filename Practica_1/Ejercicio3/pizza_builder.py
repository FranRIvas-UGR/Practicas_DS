from abc import ABC, abstractmethod
import tkinter as tk

class Director:
    def __init__(self, builder):
        self._builder = builder

    def make_pizza(self):
        self._builder.create_new_pizza()
        self._builder.add_dough()
        self._builder.add_sauce()
        self._builder.add_toppings()

class PizzaBuilder(ABC):
    def _init_(self):
        self.pizza = None
    
    def create_new_pizza(self):
        self.pizza = Pizza()

    @abstractmethod
    def add_dough(self):
        pass

    @abstractmethod
    def add_sauce(self):
        pass

    @abstractmethod
    def add_toppings(self):
        pass

class MargheritaPizzaBuilder(PizzaBuilder):
    def add_dough(self):
        self.pizza.dough = "Thin crust"

    def add_sauce(self):
        self.pizza.sauce = "Tomato sauce"

    def add_toppings(self):
        self.pizza.toppings = ["Mozzarella cheese", "Fresh basil"]

class PepperoniPizzaBuilder(PizzaBuilder):
    def add_dough(self):
        self.pizza.dough = "Thick crust"

    def add_sauce(self):
        self.pizza.sauce = "Tomato sauce"

    def add_toppings(self):
        self.pizza.toppings = ["Pepperoni", "Mozzarella cheese", "Mushrooms", "Onions"]

class VeggiePizzaBuilder(PizzaBuilder):
    def add_dough(self):
        self.pizza.dough = "Thin crust"

    def add_sauce(self):
        self.pizza.sauce = "Tomato sauce"

    def add_toppings(self):
        self.pizza.toppings = ["Mushrooms", "Bell peppers", "Onions", "Black olives", "Spinach"]

class Pizza:
    def __init__(self):
        self.dough = None
        self.sauce = None
        self.toppings = None

    def __str__(self):
        return f"Pizza specs:\nDough: {self.dough}\nSauce: {self.sauce}\nToppings: {', '.join(self.toppings)}"


def make_pizza(builder):
    director = Director(builder)
    director.make_pizza()
    return builder.pizza

def make_margherita():
    return make_pizza(MargheritaPizzaBuilder())

def make_pepperoni():
    return make_pizza(PepperoniPizzaBuilder())

def make_veggie():
    return make_pizza(VeggiePizzaBuilder())

def display_pizza(pizza):
    result_label.config(text=str(pizza))

root = tk.Tk()
root.title("Pizza Builder")

margherita_button = tk.Button(root, text="Margherita", command=lambda: display_pizza(make_margherita()))
margherita_button.pack()

pepperoni_button = tk.Button(root, text="Pepperoni", command=lambda: display_pizza(make_pepperoni()))
pepperoni_button.pack()

veggie_button = tk.Button(root, text="Veggie", command=lambda: display_pizza(make_veggie()))
veggie_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()