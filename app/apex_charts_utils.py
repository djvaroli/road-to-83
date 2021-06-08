from typing import *


def line_series_dict(
        name: str,
        data: List
) -> Dict:
    config = {
        "name": name,
        "type": "line",
        "data": data
    }

    return config