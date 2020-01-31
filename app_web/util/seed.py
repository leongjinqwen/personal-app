from models.category import Category
from models.expense import Expense



def change_cat():
    food = Category.get(Category.name=='Food')
    transport = Category.get(Category.name=='Transport')
    general = Category.get(Category.name=='General')
    ent = Category.get(Category.name=='Entertainment')
    Expense.update(cat=food).where(Expense.category=='Food').execute()
    Expense.update(cat=transport).where(Expense.category=='Transport').execute()
    Expense.update(cat=ent).where(Expense.category=='Entertainment').execute()
    Expense.update(cat=general).where(Expense.category=='General').execute()