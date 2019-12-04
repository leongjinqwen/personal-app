from datetime import date

def register_jinja_filters(app):
    @app.context_processor
    def inject_today_date():
        return {'today_date': date.today().strftime("%B %Y")}

    @app.context_processor
    def inject_today():
        return {'today': date.today().strftime("%d %B %Y")}