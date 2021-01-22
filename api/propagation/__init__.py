import requests
from xml.etree import ElementTree
from datetime import datetime

from ..util.xml import XmlDictConfig


def _fetchPropagationData() -> dict:

    # Fetch propagation XML data
    resp = requests.get("http://www.hamqsl.com/solarxml.php")

    # Handle possible error
    if int(resp.status_code / 100) != 2:
        return None

    # Parse to dict
    etree = ElementTree.XML(resp.text)
    return XmlDictConfig(etree)


def _getSolarImagesDict() -> dict:
    return {
        "hmi": {
            "intensitygram": {
                "4096": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_HMIIF.jpg",
                "2048": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_2048_HMIIF.jpg",
                "1024": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
                "512": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_HMIIF.jpg",
            },
            "magnetogram": {
                "4096": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_HMIBC.jpg",
                "2048": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_2048_HMIBC.jpg",
                "1024": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",
                "512": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_HMIBC.jpg",
            }
        },
        "aia": {
            "normal": {
                "4096": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_211193171.jpg",
                "2048": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_2048_211193171.jpg",
                "1024": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_211193171.jpg",
                "512": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_211193171.jpg",
            },
            "pfss": {
                "4096": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_211_193_171pfss.jpg",
                "2048": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_211_193_171pfss_2048.jpg",
                "1024": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_211_193_171pfss_1024.jpg",
                "512": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_211_193_171pfss_512.jpg",
            }
        }

    }


def doPropagationReport() -> dict:

    # Get solar images
    solar_images = _getSolarImagesDict()

    # Get unformatted propagation data
    propagation_data = _fetchPropagationData()

    # Create a base dict
    output = {}

    # If the propagation data is valid, add and format it
    if propagation_data:
        output.update({
            "updated": datetime. strptime(propagation_data["solardata"]["updated"].strip(), "%d %b %Y %H%M GMT"),
            "noise_floor": propagation_data["solardata"]["signalnoise"],
            "solar": {
                "status": {
                    "geomagnetic_field": propagation_data["solardata"]["geomagfield"],
                    "k_index": propagation_data["solardata"]["kindexnt"],
                    "muf": propagation_data["solardata"]["muf"],
                },
                "sunspot_count": int(propagation_data["solardata"]["sunspots"]),
                "wind": float(propagation_data["solardata"]["solarwind"]),
                "flux": int(propagation_data["solardata"]["solarflux"]),
                "proton_flux": int(propagation_data["solardata"]["protonflux"]),
                "normalization": float(propagation_data["solardata"]["normalization"]),
                "muf_factor": float(propagation_data["solardata"]["muffactor"]),
                "magnetic_field": float(propagation_data["solardata"]["magneticfield"].strip()),
                "lat_degree": float(propagation_data["solardata"]["latdegree"]),
                "k_index": float(propagation_data["solardata"]["kindex"].strip()),
                "helium_line": float(propagation_data["solardata"]["heliumline"]),
                "fof2": float(propagation_data["solardata"]["fof2"]),
                "electron_flux": float(propagation_data["solardata"]["electonflux"]),
                "aurora": float(propagation_data["solardata"]["aurora"].strip()),
                "a_index": float(propagation_data["solardata"]["aindex"].strip()),
            },
            "band_conditions": {
                "hf": {
                    "day": {
                        "80m": propagation_data["solardata"]["calculatedconditions"]["band"][0],
                        "40m": propagation_data["solardata"]["calculatedconditions"]["band"][0],
                        "30m": propagation_data["solardata"]["calculatedconditions"]["band"][1],
                        "20m": propagation_data["solardata"]["calculatedconditions"]["band"][1],
                        "17m": propagation_data["solardata"]["calculatedconditions"]["band"][2],
                        "15m": propagation_data["solardata"]["calculatedconditions"]["band"][2],
                        "12m": propagation_data["solardata"]["calculatedconditions"]["band"][3],
                        "10m": propagation_data["solardata"]["calculatedconditions"]["band"][3],
                    },
                    "night": {
                        "80m": propagation_data["solardata"]["calculatedconditions"]["band"][4],
                        "40m": propagation_data["solardata"]["calculatedconditions"]["band"][4],
                        "30m": propagation_data["solardata"]["calculatedconditions"]["band"][5],
                        "20m": propagation_data["solardata"]["calculatedconditions"]["band"][5],
                        "17m": propagation_data["solardata"]["calculatedconditions"]["band"][6],
                        "15m": propagation_data["solardata"]["calculatedconditions"]["band"][6],
                        "12m": propagation_data["solardata"]["calculatedconditions"]["band"][7],
                        "10m": propagation_data["solardata"]["calculatedconditions"]["band"][7],
                    }
                },
                "vhf": {
                    "northern_hemisphere": propagation_data["solardata"]["calculatedvhfconditions"]["phenomenon"][0],
                    "north_america": propagation_data["solardata"]["calculatedvhfconditions"]["phenomenon"][2],
                    "eurpoe": {
                        "e_skip": propagation_data["solardata"]["calculatedvhfconditions"]["phenomenon"][1],
                        "e_skip_6m": propagation_data["solardata"]["calculatedvhfconditions"]["phenomenon"][3],
                        "e_skip_4m": propagation_data["solardata"]["calculatedvhfconditions"]["phenomenon"][4],
                    }
                }
            },
        })

    # Add images
    if "solar" not in output:
        output["solar"] = {}
    output["solar"]["images"] = solar_images

    return output
