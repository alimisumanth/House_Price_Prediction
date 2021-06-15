import sqlite3
import pandas as pd
from io import StringIO
from sklearn.model_selection import train_test_split
import pickle


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
        return df.to_html(classes='mystyle')


def model_training():
    with sqlite3.connect("db.sqlite3") as c:
        table = pd.read_sql_query('SELECT * from boston', c)
        x = table.drop(['medv', 'index'], axis=1)
        print(x.head(2))
        model = pickle.load(open('boston_data.pkl', 'rb'))
        prediction = model.predict(x)
        x['prediction'] = prediction
        return x.to_html()
