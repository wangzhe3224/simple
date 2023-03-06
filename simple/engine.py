from __future__ import annotations  # the FUTURE of annotation...hah 

from collections import defaultdict
from typing import Any, Dict, List, Callable
from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep
import logging
from threading import Thread

from simple.event_bus import EventBus
from simple.model import Event, EventType, Bar, Order, Trade, OrderType, Asset, AssetType
from simple.data.core import DataFeed


LOG = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(consoleHandler)
LOG.setLevel(logging.DEBUG)


class Engine:

    def __init__(self, bus: EventBus, strategy: Strategy, feed: DataFeed, execution: Execution):
        self.bus = bus
        self.strategy = strategy
        self.feed = feed
        self.execution = execution

    def run(self):
        # subs
        self.bus.subscribe(EventType.BAR, self.strategy.on_bar)
        self.bus.subscribe(EventType.ORDER_CREATE, self.execution.on_order_create)
        self.bus.start()
        self.feed.start()
        
        while True:
            sleep(0.05)


class Execution(ABC):

    @abstractmethod
    def submit_order(self, order: Order) -> int:
        ...

    @abstractmethod
    def cancel_order(self, order_id: int):
        ...

    @abstractmethod
    def modify_order(self, order_id: int, order: Order):
        ...

    @abstractmethod
    def on_order_create(self, order: Order):
        ...

    @abstractmethod
    def start(self):
        ...
    

class DummyExecution(Execution):
    
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus

    def submit_order(self, order: Order) -> int:
        return super().submit_order(order)

    def cancel_order(self, order_id: int):
        return super().cancel_order(order_id)

    def modify_order(self, order_id: int, order: Order):
        return super().modify_order(order_id, order)

    def on_order_create(self, order: Order):
        LOG.info(f"Execution recieved {order =  }")
        
    def start(self):
        return super().start()


# 2. I write down strategy class
class Strategy:

    def __init__(self, bus: EventBus) -> None:
        self.bus = bus

    def on_bar(self, bar: Bar):
        latency = datetime.now() - bar.timestamp
        LOG.info(f"Strategy reveived {bar} with latency {latency.microseconds / 1000} ms")
        LOG.info(f"Computing some fancy signal ...")
        LOG.info(f"Submit Order...")
        self.submit_order()
    
    def submit_order(self):
        order = Order(
            asset=Asset(AssetType.CASH, name="Bitcoin"), 
            type=OrderType.MARKET,
            price=-1,
            amount=1.0,
        )
        event = Event(
            EventType.ORDER_CREATE,
            payload=order
        )
        self.bus.push(event)