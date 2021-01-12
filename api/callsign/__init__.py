from .rbn import getRBNSpotsForCall, getDXCCSpotsForCall
from .qrz import getQRZInfoForCall
from .hamqth import getHamQTHInfoForCall


def doCallsignQuery(callsign: str) -> dict:

    # Get all spots
    spots = list(getRBNSpotsForCall(callsign))
    spots += list(getDXCCSpotsForCall(callsign))

    # Get QRZ info
    qrz_info = getQRZInfoForCall(callsign)

    # Get HamQTH info
    hamqth_info = getHamQTHInfoForCall(callsign)

    return {
        "name": hamqth_info.name,
        "lookups": qrz_info.lookups + hamqth_info.lookups,
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
