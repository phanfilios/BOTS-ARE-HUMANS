import threading

class Bot(threading. thread):
  def_int_(self, name,bus,topic=None):
    super()_int_(daemon=True)
  self.name = name
  self.bus = bus
  self._stop_event=threading.Event()
      if topics:
            for t in topics:
                bus.subscribe(t, self.handle_message)

    def publish(self, topic, payload):
        self.bus.publish(topic, payload)

    def handle_message(self, msg):
        pass

    def stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    def run(self):
        raise NotImplementedError("El bot necesita implementar run().")
