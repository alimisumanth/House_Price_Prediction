import sqlite3
import pandas as pd
from io import StringIO, BytesIO
from pandas_profiling import ProfileReport
from django.http import HttpResponse


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
        return df.to_html(classes='mystyle')  #


def statisticalinfo():
    with sqlite3.connect("db.sqlite3") as c:
        table = pd.read_sql_query('SELECT * from boston', c)
        prof = ProfileReport(table, title='Demo Project')
        prof.to_file(output_file='templates/eda.html')

def tabledeletion():
    with sqlite3.connect("db.sqlite3") as c:
        cur = c.cursor()
        try:
            cur.execute("DROP TABLE boston")
            c.commit()
        except:
            pass



def filedownload():
    try:
        with sqlite3.connect("db.sqlite3") as c, BytesIO() as b:
            df = pd.read_sql_query('SELECT * from boston', c)
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            # Set up the Http response.
            filename = 'boston.xlsx'
            response = HttpResponse(
                   b.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
    except Exception as e:
        return e
