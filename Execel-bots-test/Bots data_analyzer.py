from core.bot_base import Bot

class DataAnalyzerBot(Bot):
  def_int_(self, name. bus):
           super()._int_(name, bus, topics=["sensor,data"])
  def handle_message(self, msg):
      valor msg.payload["valor"]

  if valor > 50:
    alerta = {
      "mensaje.f"valor alto detectado: {valor: .2f}"
      }
      print(f"[{self.name}] Alerta → {alerta}")
      self.publish("alert", alerta)
