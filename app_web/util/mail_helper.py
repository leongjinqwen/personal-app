import os
from app_web import sg
from sendgrid.helpers.mail import *
import pdfkit
from models.user import User
from models.expense import Expense
from models.statement import Statement
from models.category import Category
import tempfile
import subprocess
from .aws_uploader import upload_image_to_s3
import datetime
from peewee import fn
from flask import render_template

def create_statement(month=None):
  def _get_pdfkit_config():
    if os.getenv('FLASK_ENV') == 'production':
      WKHTMLTOPDF_CMD = subprocess.Popen(
        ['which', os.environ.get(
          'WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')],
        stdout=subprocess.PIPE).communicate()[0].strip()
      return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    else:
      return pdfkit.configuration()

  def create_pdf(pdf_content, filename):
    options = {
      'margin-top': '0mm',
      'margin-bottom': '0mm',
      'margin-left': '0mm',
      'margin-right': '0mm',
      'page-size': 'A4',
      'page-width': '210mm',
      'page-height': '296mm'
    }
    pdf = pdfkit.from_string(
      pdf_content, False, configuration=_get_pdfkit_config(), options=options)
    temp_file = tempfile.TemporaryFile()
    temp_file.filename = filename
    temp_file.content_type = "application/pdf"
    temp_file.write(pdf)
    temp_file.seek(0)
    return temp_file

  if month == None :
    year = datetime.datetime.now().year
    full_month = datetime.date.today().strftime("%B %Y") # current month
    short_month = datetime.date.today().strftime("%b")
  else:
    # '2020-12' convert to 'December 2020'
    year_month = month.split('-') # ['2020','12']
    year = int(year_month[0])
    short_month = datetime.datetime(year, int(year_month[1]), 1).strftime("%b")
    full_month = datetime.datetime(year, int(year_month[1]), 1).strftime("%B %Y")

  # select all user from database
  users = User.select()
  # get all expenses to render in template
  for user in users:
    record = Statement.get_or_none(Statement.user==user.id, Statement.month==full_month)
    if not record:
      expenses = Expense.select().where(Expense.cat in user.categories, Expense.month == short_month, Expense.created_at.year == year).order_by(Expense.created_at.asc())
      # ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.cat in user.categories, Expense.month == short_month, Expense.created_at.year == year)
      total = 0
      for exp in expenses:
        total += exp.amount

      html = render_template('expenses/statement.html', expenses=expenses, total=total, month=str(full_month))
      pdf_name = (user.username).replace(" ", "-").lower() + "-" + str(full_month).replace(" ", "-")
      temp_file = create_pdf(html, pdf_name)
      statement_url = upload_image_to_s3(user.id ,temp_file)
      print(statement_url)

      statement = Statement(user=user.id, exp_url=statement_url, month=full_month)
      statement.save()
      '''
      Send monthly statement email
      '''
      # message = Mail(
      #   from_email="leongjinqwen@gmail.com",
      #   to_emails=user.email,
      #   subject=f"{month} Expenses Statement",
      #   html_content=Content("text/html", f"<h1>Dear {user.username},</h1><br/>Here is your expenses statement PDF.<br/><a href={statement_url}>{month} Statement<a><br/><h1>Jw</h1>")
      # )
      # try:
      #   response = sg.send(message)
      #   print(response.body)
      # except Exception as e:
      #   print(str(e))
    else:
      print('already exist!')

