from __future__ import print_function
from random import randint
from random import uniform
from random import choice
import logging
import sys
import time

import grpc
import TemperatureService_pb2
import TemperatureService_pb2_grpc

import const

# Generate a date between 01/01/1970 and 31/12/2022
def date_gerenator():
    year = randint(1970, 2022)
    month = randint(1, 12)
    if month == (1 or 3 or 5 or 7 or 8 or 10 or 12):
        day = randint(1, 31)
    elif month == (4 or 6 or 9 or 11):
        day = randint(1, 30)
    elif (year % 4 == 0):
        day = randint(1, 29)
    else:
        day = randint(1, 28)
    return day, month, year

# Choose a location among some Brazilian capitals
def location_generator():
    locations = ['Goiania', 'Sao Paulo', 'Brasilia', 'Rio de Janeiro']
    return choice(locations)

# Generate a temperature between 24 and 40 Celsius
def temperature_generator():
    temp = str(round(uniform(24, 40), 1)) + ' C'
    return temp

def run():
    # Get the client function, query or generate
    try:
        function = int(sys.argv[1])
    except:
        print ('Usage: python3 EmployeeClient.py <function_number>')
        exit(1)

    with grpc.insecure_channel(const.IP+':'+const.PORT) as channel:
        stub = TemperatureService_pb2_grpc.TemperatureServiceStub(channel)

        # Query temperatures
        if function == 1:
            while (True):
                query = int(input('Query by Date(1) or Location(2)?\nEnter the number: '))
                
                # Query all temperatures for a certain date
                if query == 1:
                    day_aux, month_aux, year_aux = input('Enter date (DD/MM/YYYY)\n').split('/')
                    date_aux = TemperatureService_pb2.Date(day=int(day_aux), month=int(month_aux), year=int(year_aux))
                    response = stub.GetTempFromDate(date_aux)
                    print ('All temperatures in ' + str(day_aux) +'/' + str(month_aux) + '/' + str(year_aux) + \
                        ': ' + str(response))

                # Query all temperatures for a certain location
                elif query == 2:
                    location_aux = input('Enter location (Goiania, Sao Paulo, Brasilia or Rio de Janeiro)\n')
                    response = stub.GetTempFromLocation(TemperatureService_pb2.Location(location=location_aux))
                    print ('All temperatures in ' + location_aux + ': ' + str(response))

        # Generate new temperatures
        elif function == 2:
            while (True):
                day_aux, month_aux, year_aux = date_gerenator()
                location_aux = location_generator()
                temperature_aux = temperature_generator()
                date_aux = TemperatureService_pb2.Date(day=day_aux, month=month_aux, year=year_aux)
                data = TemperatureService_pb2.TemperatureData(date=date_aux, location=location_aux, 
                        temperature=temperature_aux)
                # Add a new temperature
                response = stub.RegisterTemp(data)
                print ('Added new temperature ' + response.status)
                time.sleep(1)



if __name__ == '__main__':
    logging.basicConfig()
    run()