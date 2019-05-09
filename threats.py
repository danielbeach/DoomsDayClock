import requests
from xml.etree import ElementTree
from datetime import datetime
import os

def iter_alerts(tree):
    for alert in tree:
        if alert.attrib:
            for k, v in alert.items():
                if k == 'type':
                    yield v
                else:
                    pass



def threats():
    result = requests.get('http://www.dhs.gov/ntas/1.1/alerts.xml')
    tree = ElementTree.fromstring(result.content)
    alerts = iter_alerts(tree)
    threat_list = []
    for a in alerts:
        threat_list.append(a)
    if threat_list:
        return threat_list
    else:
        threat_list = ['test threat']
        return threat_list



def main():
    cwd = os.getcwd()
    date = datetime.now()
    filename = 'threats-{year}-{month}-{day}-{minute}'.format(year=date.year, month=date.month, day=date.day, minute=date.minute)
    file = open("{cwd}/doomsday/threats/{file_name}.txt".format(cwd=cwd,file_name=filename), "a")
    threat_list = threats()
    for threat in  threat_list:
        file.write(str(threat) + ', \n')
    file.close()


if __name__ == '__main__':
    main()
