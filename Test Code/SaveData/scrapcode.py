# s = 'http://www.google.com/'
# s = 'https://futurism.com/new-research-shows-that-time-travel-is-mathematically-possible/'
#
# if '://' in s:
#     print s[s.find(':')+3:]

from collections import OrderedDict


records = [{u'Name': u'North America', u'Address': u'104.160.131.3'},
          {u'Name': u'Latin America North', u'Address': u'192.168.0.1'},
          {u'Name': u'Test', u'Address': u'http://www.google.com'}]


def add_rec(name, addr):
    # order =
    values = [name, addr]
    # records[0] = collections.OrderedDict(records[0])
    # print records[0]
    # new_rec = dict((key, values[ord_record.keys().index(key, 0)]) for key in ord_record.keys())
    # print new_rec
    keys = ["Name", "Address"]
    new_rec = OrderedDict((key, values[keys.index(key, 0)]) for key in keys)
    records.append(new_rec)
    print records

add_rec('Test2', 'youtube.com')
