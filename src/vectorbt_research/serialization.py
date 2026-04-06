from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if isinstance(value, pd.Timedelta):
        return value.isoformat()

    if isinstance(value, pd.Series):
        return {str(key): to_jsonable(item) for key, item in value.items()}

    if isinstance(value, pd.DataFrame):
        records = value.to_dict("records")
        return [{str(key): to_jsonable(item) for key, item in row.items()} for row in records]

    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [to_jsonable(item) for item in value]

    return str(value)
