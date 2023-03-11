from __future__ import annotations

from collections import defaultdict
from threading import Thread
from time import sleep
from typing import Dict, List, Callable
import logging

from simple.model import EventType, Event

LOG = logging.getLogger(__name__)


class EventBus:

    def __init__(self, sample_freq: float=0.2):
        self.topics: Dict[EventType, List[Callable]] = defaultdict(list)   # TODO: Could be a priority queue
        self.events: List[Event] = list()
        self.sample_freq = sample_freq
        self.thread = Thread(target=self.blocking_run)

    def subscribe(self, event_type: EventType, callback: Callable):
        LOG.debug(f"Subscribe {event_type} with {callback}")
        self.topics[event_type].append(callback)  # TODO: could be duplicated callbacks.

    def push(self, event: Event):
        self.events.append(event)

    def blocking_run(self):
        """ blocking run """
        while True:
            while self.events:
                event = self.events.pop()
                _callables = self.topics[event.type]
                for _callable in _callables:
                    _callable(event.payload)

            sleep(self.sample_freq)  # sample frequency to avoid throttling the CPU.

    def start(self):
        """ Async run """
        LOG.info(f"EventBus thread starting...")
        self.thread.start()

    def stop(self):
        self.thread.join()
