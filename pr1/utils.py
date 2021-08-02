from io import BytesIO
from docx import Document
from django.http import HttpResponse
import sqlite3
import pandas as pd



def featuresinfo_download():
    document = Document()
    document.add_heading('Document Title', 0)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=data_description.docx'
    document.save(response)

    return response

def filedownload():
    try:
        with sqlite3.connect("db.sqlite3") as c, BytesIO() as b:
            df = pd.read_sql_query('SELECT * from predicted_House_pricing', c)
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            # Set up the Http response.
            filename = 'House_pricing.xlsx'
            response = HttpResponse(
                   b.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
    except Exception as e:
        return e