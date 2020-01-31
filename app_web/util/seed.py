from models.category import Category
from models.expense import Expense


def create_cat():
    Category(name='Food',user=1).save()
    Category(name='Transport',user=1).save()
    Category(name='Entertainment',user=1).save()
    Category(name='General',user=1).save()


# def change_cat():
#     food = Category.get(Category.name=='Food')
#     transport = Category.get(Category.name=='Transport')
#     general = Category.get(Category.name=='General')
#     ent = Category.get(Category.name=='Entertainment')
#     Expense.update(category=food).where(Expense.category=='Food').execute()
#     Expense.update(category=transport).where(Expense.category=='Transport').execute()
#     Expense.update(category=ent).where(Expense.category=='Entertainment').execute()
#     Expense.update(category=general).where(Expense.category=='General').execute()