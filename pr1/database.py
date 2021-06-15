import sqlite3
import pandas as pd
from io import StringIO

#table creation
def tablecreation(request):
    with sqlite3.connect("db.sqlite3") as c:
        cur=c.cursor()
        name = request.FILES["file"]
        file=name.read().decode('utf-8')
        data = StringIO(file)
        df = pd.read_csv(data)
        df.to_sql('titanic', c,if_exists='replace')
        c.commit()
        return {'data': df.to_html(max_cols=12)}
def modeltraining(request):
    with sqlite3.connect("db.sqlite3") as c:
        cur=c.cursor()
        table=pd.read_sql_query('SELECT * from titanic',c)
        print(table.head(5))
        print(type(table))
        return {"result":"ok"}









