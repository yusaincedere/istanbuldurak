import zeep
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
from requests import Session
from datetime import date

session = Session()

HatDurakAyrinti = 'https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl'
Duraklar = 'https://api.ibb.gov.tr/iett/UlasimAnaVeri/HatDurakGuzergah.asmx?wsdl'
SeferSaat = 'https://api.ibb.gov.tr/iett/UlasimAnaVeri/PlanlananSeferSaati.asmx?wsdl'
SeferDurum = 'https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl'
GorevZaman = 'https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl'
Duyurular = 'https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl'


def getHatXml(val):
    client = zeep.Client(wsdl=HatDurakAyrinti)
    data = client.service.HatServisi_GYY(val)
    return data


def XmlToJsonOne(element):
    if element.text == None and len(element.attrib):
        return element.tag, element.attrib
    return element.tag, \
           dict(map(XmlToJsonOne, element)) or element.text


def HatXmlToJson(data):
    list = []
    for val in data:
        list.append(XmlToJsonOne(val))
    return list


def getDurakDetayXml(val):
    client = zeep.Client(wsdl=HatDurakAyrinti)
    data = client.service.DurakDetay_GYY(val)
    return data


def DurakXmlToJson(data):
    list = []
    for val in data:
        list.append(
            {
                "HATKODU": "{}".format(XmlToJsonOne(val[0])[1]),
                "YON": "{}".format(XmlToJsonOne(val[1])[1]),
                "SIRANO": "{}".format(XmlToJsonOne(val[2])[1]),
                "SDURAKKODU": "{}".format(XmlToJsonOne(val[3])[1]),
                "SDURAKADI": "{}".format(XmlToJsonOne(val[4])[1]),
                "XKOORDINATI": "{}".format(XmlToJsonOne(val[5])[1]),
                "YKOORDINATI": "{}".format(XmlToJsonOne(val[6])[1]),
                "ILCEADI": "{}".format(XmlToJsonOne(val[9])[1])
            }
        )
    return list


def getDuraklar(val):
    client = zeep.Client(wsdl=Duraklar)
    data = client.service.GetDurak_json(val)
    return data




def getSeferKonum(val):
    client = zeep.Client(wsdl=SeferDurum)
    data = client.service.GetHatOtoKonum_json(val)
    return data


def FiloSeferKonum():
    client = zeep.Client(wsdl=SeferDurum)
    data = client.service.GetFiloAracKonum_json()
    return data




