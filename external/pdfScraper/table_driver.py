"""
table_driver.py: The purpose of this file is to develop the entire journal scraper functionality with the touch of a button. This
is simply meant to help develop python parts of the web application. This is not ship-able code.

__authors__ = "Joshua Johnson"
__version__ = "1.0"
__email__ = "jdjohn43@asu.edu"
__date__ = "11/7/18"
"""

import PyPDF2
from tabula import read_pdf
import re
import sys
from copy import deepcopy
import json
import pdf_text_import as pti
import table_cleaner as tc
import table_page_finder as tpf

pdf = ["pdfs/WassonandRichardson_GCA_2011.pdf",
       "pdfs/WassonandChoe_GCA_2009.pdf",
       "pdfs/Wasson_GCA_2017.pdf",
       "pdfs/WassonandChoi_2003.pdf",
       "pdfs/Litasov2018_Article_TraceElementCompositionAndClas.pdf",
       "pdfs/Wasson_2010.pdf",
       "pdfs/Wasson_2004.pdf",
       "pdfs/Wassonetal_GCA_2007.pdf",
       "pdfs/Ruzicka2014.pdf",
       "pdfs/WassonandKallemeyn_GCA_2002.pdf",
       "pdfs/RuzickaandHutson2010.pdf"]

fileName = pdf[9]
# print(fileName)

# j = json.loads(sys.argv[1])
# fileName = j['fileName']
# fileName = '/usr/app/controller/py/WassonandChoe_GCA_2009.pdf'
# pageNum = int(j['pageNum'])
# taskNum = int(j['taskNum'])
# flipDir = int(j['flipDir'])
# coordsLeft = j['coordsLeft']
# coordsTop = j['coordsTop']
# coordsWidth = j['coordsWidth']
# coordsHeight = j['coordsHeight']


tables = []
json_pages_confirmed = []

# START Get number of Pages
total_pages = PyPDF2.PdfFileReader(open(fileName, 'rb')).numPages

# START get text from pdf
text = pti.convert_pdf_to_txt_looper(fileName, total_pages)

# START Finding pages that have tables on them.
json_pages = tpf.find_pages_with_tables(total_pages, text)

# START Get tables 1 page at a time.
for page in range(len(json_pages)):
    one_page_of_tables = read_pdf(fileName, output_format="dataframe", encoding="utf-8", multiple_tables=True,
                                  pages=json_pages[page]["pdf_page"], silent=True)
    if one_page_of_tables:
        for table in one_page_of_tables:
            tables.append(table)
            json_pages_confirmed.append(json_pages[page])


# START Make sure tables exist on pages.
# json_master_pages_with_tables_confirmed = confirm_tables_exist()

# START Make a pristine copy of list of tables before mark up.
tables_pristine = deepcopy(tables)

# START Marking the fields for removal
tc.mark_fields_for_removal(tables)

# START removing rows of bad data
for ind in range(len(tables)):
    tables[ind], tables_pristine[ind] = tc.row_by_row(tables[ind], tables_pristine[ind])

# Remove dead tables from list after row by row
tc.empty_table_remover(tables, tables_pristine, json_pages_confirmed)

# START removing cols of bad data
for ind in range(len(tables)):
    tables[ind], tables_pristine[ind] = tc.column_by_column(tables[ind], tables_pristine[ind])

# Remove dead tables from list after col by col
tc.empty_table_remover(tables, tables_pristine, json_pages_confirmed)


# Put original values back in fields marked for removal by mistake
tc.marked_field_clean_up(tables, tables_pristine)

for ind in range(len(tables)):
    tables[ind] = '{\"actual_page\":' + str(json_pages_confirmed[ind]["actual_page"]) \
                  + ',\"pdf_page\": ' + str(json_pages_confirmed[ind]["pdf_page"]) \
                  + ', \"Table\":' + tables[ind].to_json() + '}'
    # print(tables[ind])
print(tables)
