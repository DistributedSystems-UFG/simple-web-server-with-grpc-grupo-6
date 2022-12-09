from concurrent import futures
import logging

import grpc
import TemperatureService_pb2
import TemperatureService_pb2_grpc

temperatureDB=[]

class TemperatureServer(TemperatureService_pb2_grpc.TemperatureServiceServicer):

  def RegisterTemp(self, request, context):
    dat = {
      'date':{
        'day':request.date.day,
        'month':request.date.month,
        'year':request.date.year
      },
      'location':request.location,
      'temperature':request.temperature
    }
    temperatureDB.append(dat)
    return TemperatureService_pb2.StatusReply(status='OK')

  def GetTempFromDate(self, request, context):
    list = TemperatureService_pb2.TemperatureResponse()
    for item in temperatureDB:
      if item['date']['day'] == request.day and item['date']['month'] == request.month and \
        item['date']['year'] == request.year:
        temperature_data = TemperatureService_pb2.TemperatureData(date=item['date'], 
                            location=item['location'], temperature=item['temperature'])
        list.temps.append(temperature_data)
    return list

  def GetTempFromLocation(self, request, context):
    list = TemperatureService_pb2.TemperatureResponse()
    for item in temperatureDB:
      if item['location'] == request.location:
        temperature_data = TemperatureService_pb2.TemperatureData(date=item['date'], 
                            location=item['location'], temperature=item['temperature'])
        list.temps.append(temperature_data)
    return list

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    TemperatureService_pb2_grpc.add_TemperatureServiceServicer_to_server(TemperatureServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()