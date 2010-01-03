from mailer import Mailer
from mailer import Message
import html2text
import csv
import smtplib

from_ = "fjsanchezm@cotemar.com.mx"
to = "rorozco@cotemar.com.mx"
header = ["UserName","Password","Descripcion","ClaveSAP","Perfil","Email"]
file_send =csv.DictWriter(open("send.csv","w"),header)
file_notsend =csv.DictWriter(open("notsend.csv","w"),header)
file_fail =csv.DictWriter(open("fail.csv","w"),header)
#sender = Mailer(host="cot-cdc-mail01")
sender = Mailer(host="localhost",port=8007)
file =open("cotpag.html")
str_html_back = file.read()
csv_file = csv.DictReader(open("BD.csv"))

for d in csv_file:
    if int(d["Perfil"]) is not 2:
        file_notsend.writerow(d)
        to =""
        continue
    if not "@" in d["Email"]:
        file_notsend.writerow(d)
        to=""
        continue
    else:
        to = d["Email"]

    m = Message(From= from_, To = to)
    m.attach("cote.gif","header")
    params = dict(
        razon_social=d["Descripcion"],
        numero_sap=d["ClaveSAP"],
        userid=d["UserName"],
        password=d["Password"]
    )
    str_html = str_html_back % params
    m.Subject = "NUEVA PAGINA WEB DE PROVEEDORES"

    m.Html = str_html
    m.Body = html2text.html2text(str_html).encode("utf8")
    try:
        sender.send(m)
        print "%s %s send"  % ( d["Email"], d["UserName"])
        file_send.writerow(d)
    except:
        print "%s %s not send "  % ( d["Email"], d["UserName"])
        file_fail.writerow(d)
