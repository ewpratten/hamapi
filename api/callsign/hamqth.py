import re
import requests
from dataclasses import dataclass
from typing import *


@dataclass
class HamQTHInfo:

    name: str
    gridsquare: str
    gridsquare_url: str
    qth: str
    lookups: int
    itu: int
    cq: int


def getHamQTHInfoForCall(callsign: str) -> HamQTHInfo:

    # Call to HamQTH
    response = requests.get(f"https://www.hamqth.com/{callsign.capitalize()}", headers={
    })

    # If no data, no info
    if int(response.status_code / 100) != 2:
        return QRZInfo(
            name=None,
            gridsquare=None,
            gridsquare_url=None,
            qth=None,
            lookups=None,
            itu=None,
            cq=None
        )

    # Content
    content = " ".join(response.text.replace("\n", "").split())

    # Fetch name
    name = re.findall(
        r'<td class="infoDesc">Name:</td><td>([a-zA-Z ]*)</td>', content)[0]
    qth = re.findall(
        r'<td class="infoDesc">QTH:</td><td>([a-zA-Z ]*)</td>', content)[0]
    gridsquare = re.findall(
        r'<td class="infoDesc">Grid:</td><td id="grid"><a href="https://aprs.fi/#\!addr=[a-zA-Z0-9]*">([a-zA-Z0-9]*)</a></td>', content)[0]
    gridsquare_url = fr"https://aprs.fi/#!addr={gridsquare}" if gridsquare else None
    itu = int(re.findall(
        r'<td class="infoDesc">ITU:&nbsp;</td><td>([0-9]*)</td>', content)[0])
    cq = int(re.findall(
        r'<td class="infoDesc">CQ:</td><td>([0-9]*)</td>', content)[0])
    lookups = int(re.findall(r'Lookups: &nbsp; ([0-9]*)', content)[0])

    return HamQTHInfo(
        name=name,
        gridsquare=gridsquare,
        gridsquare_url=gridsquare_url,
        qth=qth,
        lookups=lookups,
        itu=itu,
        cq=cq
    )
