import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

def mail_sender():
    my_email = "carlos@gmail.com"
    password = "Añadir_Password"

    connection = smtplib.SMTP("smtp.gmail.com")
    port = 587

    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs="campos@hotmail.com", msg="Subject: Look at the sky\n\n Hey the iss is just over your head!!")
    connection.close()

def iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_latitude_interval = (iss_latitude + 5, iss_latitude - 5)
    iss_longitude_interval = (iss_longitude + 5, iss_longitude - 5)



    # Your position is within +5 or -5 degrees of the ISS position.

    if iss_longitude_interval[0] >= MY_LONG >= iss_longitude_interval[1] and iss_latitude_interval[0] >= MY_LAT >= iss_latitude_interval[1]:
        return True

def night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now > sunset or time_now < sunrise:
        return True

def iss_close():
    if night() == True and iss_position() == True:
        mail_sender()


while True:
    time.sleep(60)
    iss_close()




