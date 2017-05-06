import csv


def get_addr(name):
    with open('servs.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        # reader = [
        #           {'Name': 'North America', 'Address': '104.160.131.3'},
        #           {'Name': 'Latin America North', 'Address': '192.168.0.1'}
        #          ]
        for row in reader:
            return row['Address'] if name in row['Name'] else csvfile.close()
    csvfile.close()

print get_addr('North America')
