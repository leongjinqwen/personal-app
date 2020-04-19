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
from datetime import date
from peewee import fn
from flask import render_template

def send_email():
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
        pdf = pdfkit.from_string(
            pdf_content, False, configuration=_get_pdfkit_config())
        temp_file = tempfile.TemporaryFile()
        temp_file.filename = filename
        temp_file.content_type = "application/pdf"
        temp_file.write(pdf)
        temp_file.seek(0)
        return temp_file


    # select all user from database
    users = User.select()
    # get all expenses to render in template
    for user in users:
        month = date.today().strftime("%B %Y")
        record = Statement.get_or_none(Statement.user==user.id,Statement.month==month)
        if not record:
            expenses = Expense.select().where(Expense.month==date.today().strftime("%b")).order_by(Expense.created_at.asc())
            # expenses = Expense.select().where(Expense.user==user.id,Expense.month==date.today().strftime("%b")).order_by(Expense.created_at.asc())
            # ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.user==user.id,Expense.month==date.today().strftime("%b"))
            ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.month==date.today().strftime("%b"))
            # upload to aws
            html = render_template('expenses/statement.html',expenses=expenses,ttl=ttl,cat=category.title(),month=str(month))
            pdf_name = (user.username).replace(" ", "-").lower() + "-" + str(month).replace(" ", "-")
            temp_file = create_pdf(html, pdf_name)
            statement_url = upload_image_to_s3(temp_file)
            print(statement_url)
            statement = Statement(user=user.id,exp_url=statement_url,month=month)
            statement.save()
            # send email with link
            message = Mail(
                from_email="leongjinqwen@gmail.com",
                to_emails=user.email,
                subject=f"{month} Expenses Statement",
                html_content=Content("text/html", f"<h1>Dear {user.username},</h1><br/>Here is your expenses statement PDF.<br/><a href={statement_url}>{month} Statement<a><br/><h1>Jw</h1>")
            )
            try:
                response = sg.send(message)
                print(response.body)
            except Exception as e:
                print(str(e))
        else:
            print('already exist!')

