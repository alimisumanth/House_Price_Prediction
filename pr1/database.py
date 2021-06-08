import sqlite3
import pandas as pd
from io import StringIO


def tablecreation(request):
    with sqlite3.connect("db.sqlite3") as c:
        name = request.FILES["file"]
        file=name.read().decode('utf-8')
        data = StringIO(file)
        df = pd.read_csv(data)
        df.to_sql(name.name, c,if_exists='replace')
        return {'data': df.to_html()}



