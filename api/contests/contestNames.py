import requests
import re

CONTEST_NAMES_PATTERN = r"<a target=\"_new\" href=\"https://www\.contestcalendar\.com/contestdetails\.php\?ref=\d+\">(\d+)</a></td><td>([A-Za-z\d\/., -]+) &nbsp;</td><td>([A-Za-z\d. -]+) &nbsp;</td>"


def getContestNames() -> dict:

    # Fetch contestcalendar
    resp = requests.get("https://www.contestcalendar.com/cabnames.php")

    if int(resp.status_code / 100) != 2:
        return None

    # Use regex to get all data
    contests = re.findall(CONTEST_NAMES_PATTERN, resp.text, re.M)

    return [
        {
            "id": int(contest[0]),
            "name":contest[1],
            "cabrillo_name":contest[2],
        }
        for contest in contests
    ]
