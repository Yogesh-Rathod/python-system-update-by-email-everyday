from mailer import Mailer
from mailer import Message
import schedule
import time
import psutil
from urllib2 import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()

sender = 'yogesh.rathod@loylty.in'
# , 'hardik.patel@loylty.in'
receivers = ['yogesh.rathod@loylty.in']
message = Message(From=sender, To=receivers)
message.Subject = "An HTML Email"

memoryInfo = dict(psutil.disk_usage("/")._asdict()) if psutil.disk_usage("/") else {'used': 'N.A.', 'total': 'N.A.', 'percent': 'N.A.', 'free': 'N.A.'}
print("memoryInfo ", memoryInfo);
powerInfo = dict(psutil.sensors_battery()._asdict()) if psutil.sensors_battery() else {'percent': 'N.A.', 'secsleft': 'N.A.', 'power_plugged': 'N.A.'}
print("powerInfo ", powerInfo);
temperatures = psutil.sensors_temperatures()
temperaturesObj = dict(temperatures['acpitz'][0]._asdict()) if temperatures and temperatures['acpitz'][0] else {'current': 'N.A.', 'high': 'N.A.', 'critical': 'N.A.', 'label': ''}
print("temperaturesObj ", temperaturesObj);

message.Html = """
    <p>Hi!<br>
    Here is Today's Server Details: <br>
    <h1>Server: {}</h1>

    <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>CPU Information</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th style="padding: 10px;">CPU Used</th>
                        <th style="padding: 10px;">CPU Total</th>
                        <th style="padding: 10px;">CPU Free</th>
                        <th style="padding: 10px;">Percent</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                    </tr>
                </tbody>
            </table>

            <h1>Battery Information</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th style="padding: 10px;">Percent</th>
                        <th style="padding: 10px;">Sec Left</th>
                        <th style="padding: 10px;">Power Plugged</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                    </tr>
                </tbody>
            </table>

            <h1>CPU Temperature</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th style="padding: 10px;">Current</th>
                        <th style="padding: 10px;">High</th>
                        <th style="padding: 10px;">Critical</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                        <td style="padding: 10px;">{}</td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
    """.format(my_ip, memoryInfo['used'], memoryInfo['total'], memoryInfo['free'], memoryInfo['percent'], powerInfo['percent'],  powerInfo['secsleft'], powerInfo['power_plugged'], temperaturesObj['current'], temperaturesObj['high'], temperaturesObj['critical'])



print "Server Job Starting"


def job():
    sender = Mailer('localhost')
    sender.send(message)
    print "Successfully sent email"


schedule.every().day.at("10:10:10").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
