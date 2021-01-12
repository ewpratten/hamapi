import re
import requests
from dataclasses import dataclass
from typing import *


@dataclass
class QRZInfo:

    country: str
    flag_url: str
    lookups: int


def getQRZInfoForCall(callsign: str) -> QRZInfo:

    # Call to QRZ
    response = requests.get(f"https://www.qrz.com/db/{callsign.capitalize()}", headers={
        "Host": "www.qrz.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    })

    # If no data, no info
    if int(response.status_code / 100) != 2:
        return QRZInfo(
            country=None,
            flag_url=None
        )

    # Return information
    return QRZInfo(
        country=re.findall(r"DX Atlas for: ([a-zA-Z]*)", response.text)[0],
        flag_url="https://s3.amazonaws.com/files.qrz.com/static/flags-iso/flat/32/" +
        re.findall(
            r"https://s3.amazonaws.com/files.qrz.com/static/flags-iso/flat/32/([A-Z]*).png", response.text)[0] + ".png",
        lookups = int(re.findall(r"Lookups: ([0-9]*)", response.text)[0])
    )
