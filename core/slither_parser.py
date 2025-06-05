# core/slither_parser.py
import json
import os

def parse_slither_report(address):
    path = f"slither_reports/{address}.json"
    if not os.path.isfile(path):
        return False

    data = json.load(open(path))
    for det in data.get("results", {}).get("detectors", []):
        check_name = det.get("check", "").lower()
        impact     = det.get("impact", "").lower()
        confidence = det.get("confidence", "").lower()

        # Find the first element whose "type" == "function"
        function = None
        for el in det.get("elements", []):
            if el.get("type") == "function":
                # this gives you something like "collectFees(address[])"
                function = el.get("name")
                break

        # Only pick truly high‐impact, medium/high‐confidence findings
        if impact == "high" and (confidence == "high" or confidence == "medium"):
            print(f"---> [F:{function}] [V:{check_name}] [I:{impact}] [C:{confidence}]")
            return True

    return False
