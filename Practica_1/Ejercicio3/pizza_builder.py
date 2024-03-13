from abc import ABC, abstractmethod

class Director:
    def __init__(self, builder):
        self._builder = builder

    def make_pizza(self):
        self._builder.create_new_pizza()
        self._builder.add_dough()
        self._builder.add_sauce()
        self._builder.add_toppings()

class PizzaBuilder(ABC):
    def __init__(self):
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

margherita_builder = MargheritaPizzaBuilder()
director = Director(margherita_builder)
director.make_pizza()
print(margherita_builder.pizza)

pepperoni_builder = PepperoniPizzaBuilder()
director = Director(pepperoni_builder)
director.make_pizza()
print(pepperoni_builder.pizza)

veggie_builder = VeggiePizzaBuilder()
director = Director(veggie_builder)
director.make_pizza()
print(veggie_builder.pizza)