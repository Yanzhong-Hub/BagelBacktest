# Feeder

`Feeder` is the first step in the data pipeline. It fetches data from different sources and provides the data to the next step in the pipeline. It provides `price_data` and `adjust_factor` to the next step.

## Design pattern

`Feeder` is designed to be a plugin for `BagelCore`. It is added to `BagelCore` by calling `BagelCore.add_feeder()`. The design pattern is as follows:

```mermaid
---
title: Feeder design pattern
---
classDiagram
    class Feeder{
        -_price: pd.DataFrame
        -_adjust_factor: pd.DataFrame
        -_valid_data()
        -_load_data()
        +feed() -> tuple[pd.DataFrame, pd.DataFrame]
    }

```

## Subclass

```mermaid
---
title: Feeder subclass
---
classDiagram
    class Feeder{
        -_price: pd.DataFrame
        -_adjust_factor: pd.DataFrame
        -_valid_data()
        -_load_data()
        +feed() -> tuple[pd.DataFrame, pd.DataFrame]
    }

    class DataFrameFeeder{
        -price: pd.DataFrame
        -adjust_factor: pd.DataFrame
        -_load_data()
        +feed() -> tuple[pd.DataFrame, pd.DataFrame]
    }

    class BagelDatabaseFeeder{
        -host: str
        -port: int
        -user: str
        -password: str
        -database: str
				-codes: Iterable[str]
				-start_date: datetime
				-end_date: datetime

        -_load_data()
        -_get_engine() -> Engine
        -_query_price(engine: Engine) -> pd.DataFrame
        -_query_adjust_price(engine: Engine, price: pd.DataFrame) -> pd.DataFrame
        +feed() -> tuple[pd.DataFrame, pd.DataFrame
    }

    Feeder <|-- DataFrameFeeder
    Feeder <|-- BagelDatabaseFeeder
```
