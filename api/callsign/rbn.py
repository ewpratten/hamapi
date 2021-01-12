from dataclasses import dataclass
from typing import List, Optional, Generator
import requests

@dataclass
class SpotEntry:
    
    spotted_by: str
    frequency: float
    time: str
    message: Optional[str] = None
    
def getRBNSpotsForCall(callsign: str) -> Generator[SpotEntry, None, None]:
    """Fetch all Reverse Beacon Network spots for a callsign

    Args:
        callsign (str): Callsign

    Yields:
        Generator[SpotEntry, None, None]: Spots list
    """
    
    # Build endpoint url
    endpoint = f"http://www.reversebeacon.net/dxsd1/sk.php?cdx={callsign.capitalize()}"
    fake_referrer = f"http://www.reversebeacon.net/dxsd1/dxsd1.php?f=0&t=dx&c={callsign}"
    
    # Make API call
    response = requests.get(endpoint, headers={
        "Referer": fake_referrer
    })
    
    # If no data, no spots
    if int(response.status_code / 100) != 2:
        return
    
    # Parse out each spot
    data_json = response.json()
    if "s" not in data_json: return
    for spot in data_json["s"].values():
        yield SpotEntry(
            spotted_by = spot[0],
            frequency = spot[1],
            time = spot[5]
        )
        
def getDXCCSpotsForCall(callsign: str) -> Generator[SpotEntry, None, None]:
    """Get all DXCC spots for a call

    Args:
        callsign (str): Callsign

    Yields:
        Generator[SpotEntry, None, None]: Spots list
    """
    
    # Build endpoint url
    endpoint = f"https://dxwatch.com/dxsd1/s.php?cdx={callsign.capitalize()}"
    fake_referrer = f"https://dxwatch.com/dxsd1/dxsd1.php?f=0&t=dx&c={callsign}"
    
    # Make API call
    response = requests.get(endpoint, headers={
        "Referer": fake_referrer
    })
    
    # If no data, no spots
    if int(response.status_code / 100) != 2:
        return
    
    # Parse out each spot
    data_json = response.json()
    if "s" not in data_json: return
    for spot in data_json["s"].values():
        yield SpotEntry(
            spotted_by = spot[0],
            frequency = spot[1],
            time = spot[4],
            message = spot[3]
        )