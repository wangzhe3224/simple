from simple.engine import Strategy, DummyExecution, Engine
from simple.data.core import DummyBarFeed
from simple.event_bus import EventBus

if __name__ == "__main__":

    bus = EventBus(sample_freq=0.05)
    strat = Strategy(bus)
    execution = DummyExecution(bus)
    feed = DummyBarFeed(bus)
    engine = Engine(bus, strategy=strat, feed=feed, execution=execution)

    engine.run()