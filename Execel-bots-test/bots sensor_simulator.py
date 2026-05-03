import time
import random
from ocre.Bot_Base import Bot

class SensorSimulatorBot(Bot)
      def_int_(self, nmae, bus,interval=1.0):
  super()._init_(name, bus)
  self.interval = interval

def run(self):
while not self.stopped():
data={
      "sensor_id": "sensor-1", "valor": random.uniform80,100)
      }
      print(f[{self.name}] Publicando datos: {data}")
self.publish("sensor/data", data)
time.sleep(self.interval)
