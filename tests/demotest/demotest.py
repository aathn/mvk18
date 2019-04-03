from time import sleep

latitude = 0.01
longitude = -0.1
longitude_speed = 0.01
altitude = 10000

while True:
    demoaircraft = 'fr24_callback({"x47956b":["47956B",' + str(latitude) + ','+ str(longitude) + ',80,' + str(altitude) + ',238,"2303",0,"","",1550677075,"","","",0,64,""]});'
    with open('flights.js', 'w+') as file:
        file.write(demoaircraft)
    if abs(longitude) > 0.1:
        longitude_speed = - longitude_speed
    longitude = round(longitude + longitude_speed, 4)
    sleep(5)
