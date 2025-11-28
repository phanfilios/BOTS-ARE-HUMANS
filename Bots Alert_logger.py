from core Bot_base import Bot

class AlertLoggerBot(Bot):
  def_int_(self, name , bus):
     super()._int_(name, bus, topics=["alert"])

  def handle_message(self, msg):
      print("f[{self.name}] Registrado Alertas: {msg.payload}")
    
