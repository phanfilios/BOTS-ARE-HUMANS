from .message import Message

class MessageBus:
  def_int_(self):
     self.subscribers = {}

def subscribe(self, topic, calback):
    self.subscribers.setdefault(topic,[ ]).append(callback)

def publish(self, topic, payload):
    msg = Message(topic, payload)
    for callback in
  self.subscribers.get(topic, [ ]):
               callback(msg)
