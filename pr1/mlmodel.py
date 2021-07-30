import pandas as pd
import sqlite3
import joblib


def model_training():
    with sqlite3.connect("db.sqlite3") as c:
        try:
            Y_test_original = pd.read_sql_query('SELECT * from House_pricing', c)
            print(Y_test_original.head(2))
            clf2 = joblib.load("housepredction.pkl")
            Y_test_original['years_since_update'] = Y_test_original['YearRemodAdd'] - Y_test_original['YearBuilt']
            Y_test_original['garage_value'] = Y_test_original['YearBuilt'] * Y_test_original['GarageCars']

            Y_test_original = Y_test_original.drop(columns=['GarageCars','index'])
            print(Y_test_original.head(2))

            feature_numerical_columns = [col_name for col_name in Y_test_original.columns if
                                         Y_test_original[col_name].dtype in ['int64', 'float64']]

            feature_categorical_cols = [col_name for col_name in Y_test_original.columns if
                                        Y_test_original[col_name].nunique() < 50 and
                                        Y_test_original[col_name].dtype in ['object', 'bool']]
            prediction=clf2.predict(Y_test_original)
            Y_test_original['prediction'] = prediction
            Y_test_original.to_sql('House_pricing', c, if_exists='replace')
            return {'download': 'Download', 'data': Y_test_original.to_html(classes='mystyle')}
        except Exception as e:
            return {'data': e}