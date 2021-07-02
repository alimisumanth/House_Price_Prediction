import sqlite3
import pandas as pd
from io import StringIO, BytesIO
import pickle
from pandas_profiling import ProfileReport
from django.http import HttpResponse
from io import BytesIO
import os

# table creation
def table_creation(request):
    with sqlite3.connect("db.sqlite3") as c:
        name = request.FILES["file"]
        file = name.read().decode('utf-8')
        data = StringIO(file)
        df = pd.read_csv(data, index_col=0)
        df.to_sql('boston', c, if_exists='replace')
        df.style.set_table_styles([{'selector': '',
                                    'props': [('border',
                                               '2px solid green')]}])
        c.commit()
        return df.to_html()  # class='mystyle'


def model_training():
    with sqlite3.connect("db.sqlite3") as c:
        try:
            table = pd.read_sql_query('SELECT * from boston', c)
            x = table.drop(['medv', 'index'], axis=1)
            model = pickle.load(open('boston_data.pkl', 'rb'))
            prediction = model.predict(x)
            x['prediction'] = prediction
            x.to_sql('boston', c, if_exists='replace')
            return {'download': 'Download', 'data': x.to_html()}
        except Exception as e:
            return {'data': 'Please upload the file'}




def statisticalinfo():
    with sqlite3.connect("db.sqlite3") as c:
        table = pd.read_sql_query('SELECT * from boston', c)
        prof = ProfileReport(table)
        prof.to_file(output_file='templates/eda.html')

def tabledeletion():
    with sqlite3.connect("db.sqlite3") as c:
        cur = c.cursor()
        cur.execute("DROP TABLE boston")
        c.commit()



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
