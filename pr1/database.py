import sqlite3
import pandas as pd
from io import StringIO
from pandas_profiling import ProfileReport



# table creation
def table_creation(request):
    with sqlite3.connect("db.sqlite3") as c:
        name = request.FILES["input-b6b[]"]
        file = name.read().decode('utf-8')
        data = StringIO(file)
        df = pd.read_csv(data)
        df.to_sql('House_pricing', c, if_exists='replace')
        df.style.set_table_styles([{'selector': '','props': [('border','10px solid yellow')]}])
        c.commit()
        return df.to_html(classes='input_table')  #


def statisticalinfo():
    with sqlite3.connect("db.sqlite3") as c:
        table = pd.read_sql_query('SELECT * from House_pricing', c)
        prof = ProfileReport(table, title='Demo Project')
        prof.to_file(output_file='templates/eda.html')

def tabledeletion():
    with sqlite3.connect("db.sqlite3") as c:
        cur = c.cursor()
        try:
            cur.execute("DROP TABLE House_pricing")
            cur.execute("DROP TABLE predicted_House_pricing")
            c.commit()
        except:
            pass




