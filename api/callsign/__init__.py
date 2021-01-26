from .rbn import getRBNSpotsForCall, getDXCCSpotsForCall
from .qrz import getQRZInfoForCall
from .hamqth import getHamQTHInfoForCall
import traceback


def doCallsignQuery(callsign: str) -> dict:

    # Get all spots
    spots = []
    spots += list(getRBNSpotsForCall(callsign))
    spots += list(getRBNSpotsForCall(callsign + "/QRP"))
    spots += list(getDXCCSpotsForCall(callsign))
    spots += list(getDXCCSpotsForCall(callsign + "/QRP"))

    try:
        # Get QRZ info
        qrz_info = getQRZInfoForCall(callsign)

        # Get HamQTH info
        hamqth_info = getHamQTHInfoForCall(callsign)
    except IndexError as e:
        print("An IndexError occurred. Likely was due to this callsign not being valid")
        traceback.print_tb(e.__traceback__)
        return "Callsign not found"
    
    
    return {
        "name": hamqth_info.name,
        "lookups": qrz_info.lookups + hamqth_info.lookups,
        "propagation":f"https://pskreporter.info/pskmap.html?preset&callsign={callsign.capitalize()}&txrx=tx&timerange=86400&hideunrec=1&blankifnone=1&showsnr=1&hidemax=1&showlines=1",
        "location": {
            "country": {
                "name": qrz_info.country,
                "flag_url": qrz_info.flag_url
            },
            "grid": {
                "id": hamqth_info.gridsquare,
                "url": hamqth_info.gridsquare_url
            },
            "qth": hamqth_info.qth,
            "itu": hamqth_info.itu,
            "cq": hamqth_info.cq
        },
        "spots": spots
    }
