import pyexcel as pe
import pyexcel_xlsx as pyxlsx


data = pyxlsx.get_data("servs.xlsx")
# OrderedDict(
#   [(u'Sheet1', [
#       [u'Name', u'Address'],
#       [u'North America', u'104.160.131.3'],
#       [u'Latin America North', u'192.168.0.1'],
#       [u'Test', u'http://www.google.com']
#   ])])

sheet = pe.get_sheet(file_name="servs.xlsx", name_columns_by_row=0)

# Sheet1:
# +---------------------+-----------------------+
# | Name                | Address               |
# +---------------------+-----------------------+
# | North America       | 104.160.131.3         |
# +---------------------+-----------------------+
# | Latin America North | 192.168.0.1           |
# +---------------------+-----------------------+
# | Test                | http://www.google.com |
# +---------------------+-----------------------+

cols = [col for col in sheet.columns()]
# [
#   [u'Name', u'North America', u'Latin America North', u'Test'],
#   [u'Address', u'104.160.131.3', u'192.168.0.1', u'http://www.google.com']
# ]

# rows = [row for row in sheet.rows()]
# rows = [row for row in pe.get_sheet(file_name="servs.xlsx").rows()]
# print rows[0]  # This gives ordered list of keys
# [
#   [u'Name', u'Address'],
#   [u'North America', u'104.160.131.3'],
#   [u'Latin America North', u'192.168.0.1'],
#   [u'Test', u'http://www.google.com']
# ]


book = pe.get_book(file_name="servs.xlsx")
# Sheet1:
# +---------------------+-----------------------+
# | Name                | Address               |
# +---------------------+-----------------------+
# | North America       | 104.160.131.3         |
# +---------------------+-----------------------+
# | Latin America North | 192.168.0.1           |
# +---------------------+-----------------------+
# | Test                | http://www.google.com |
# +---------------------+-----------------------+

sheet_name = book.sheet_names()[0]
# Sheet1

book_data = book.to_dict()  # same as pyxlsx.get_data("servs.xlsx") apparently
# OrderedDict(
#   [(u'Sheet1', [
#       [u'Name', u'Address'],
#       [u'North America', u'104.160.131.3'],
#       [u'Latin America North', u'192.168.0.1'],
#       [u'Test', u'http://www.google.com']
#   ])])

arr = pe.get_array(file_name="servs.xlsx")  # same as rows in sheet.rows()
# print pe.get_array(file_name="servs.xlsx")[0] # This gives ordered list of keys
# [
#   [u'Name', u'Address'],
#   [u'North America', u'104.160.131.3'],
#   [u'Latin America North', u'192.168.0.1'],
#   [u'Test', u'http://www.google.com']
# ]

bdict = pe.get_book_dict(file_name="servs.xlsx")  # same as book.to_dict()
# OrderedDict(
#   [(u'Sheet1', [
#       [u'Name', u'Address'],
#       [u'North America', u'104.160.131.3'],
#       [u'Latin America North', u'192.168.0.1'],
#       [u'Test', u'http://www.google.com']
#   ])])

gdict = pe.get_dict(file_name="servs.xlsx")
# OrderedDict(
#   [(u'Name', [u'North America', u'Latin America North', u'Test']),
#    (u'Address', [u'104.160.131.3', u'192.168.0.1', u'http://www.google.com'])])

records = pe.get_records(file_name="servs.xlsx")
# [
#   {u'Name': u'North America', u'Address': u'104.160.131.3'},
#   {u'Name': u'Latin America North', u'Address': u'192.168.0.1'},
#   {u'Name': u'Test', u'Address': u'http://www.google.com'}
# ]


def get_addr(name):
    for row in records:
        return row['Address'] if name in row['Name'] else "Error: " + str(name) + " is not in the data."

# print get_addr('North America')


# def add_rec(name, addr):
#     # print records
#     # print records[0].keys()
#
#     sheet.column["Name"] += [name]
#     index = sheet.column["Address"].index('', 0)
#     # print sheet.column["Address"].index('', 0)
#     sheet.column["Address"][3] = [addr]
#
#     # print sheet.column["Address"]
#     # sheet.save_as("servs.xlsx")
#     print sheet
#
# add_rec('Test2', 'youtube.com')

# pe.get_array(file_name="servs.xlsx")[0]


from collections import OrderedDict


def add_rec(name, addr, method=None):
    values = [name, addr]
    if method == 'safe':
        # It is still possible that the valuesa re unordered if the parameters are sent in the wrong order
        # One solution maybe is to add a prompt?
        keys = pe.get_array(file_name="servs.xlsx")[0]
        new_rec = OrderedDict((key, values[keys.index(key, 0)]) for key in keys)
        sheet.row += new_rec.values()
    else:
        sheet.row += values
    sheet.save_as("servs.xlsx")

add_rec('Test2', 'youtube.com')
