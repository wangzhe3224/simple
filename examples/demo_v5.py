from simple.engine import Strategy, DummyExecution, Engine
from simple.data.core import DummyBarFeed, BacktestBarFeed
from simple.event_bus import EventBus

if __name__ == "__main__":

    file = "./2023-2023-5m-BTCUSDT.parquet"
    bus = EventBus(sample_freq=0.05)
    strat = Strategy(bus)
    execution = DummyExecution(bus)
    feed = BacktestBarFeed(bus, file)
    # TODO: fix this. The engine will not stop! Do you know how? :X
    engine = Engine(bus, strategy=strat, feed=feed, execution=execution)

    engine.run()
