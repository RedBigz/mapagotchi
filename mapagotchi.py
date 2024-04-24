import argparse, json, os

def macify(raw):
    # https://stackoverflow.com/questions/3258573/how-to-insert-a-character-after-every-2-characters-in-a-string
    return ':'.join(raw[i:i+2] for i in range(0, len(raw), 2))

if __name__ == "__main__":
    p = argparse.ArgumentParser("mapagotchi")
    
    p.add_argument("folder")
    p.add_argument("--output", "-o", default="./mapbox.geo.json")

    ns = p.parse_args()

    out = {
        "type": "FeatureCollection",
        "features": [
        ]
    }

    for file_ in os.listdir(ns.folder):
        if not file_.endswith(".geo.json"): continue

        file = os.path.join(ns.folder, file_)

        with open(file, "r") as f:
            j = json.load(f)

            name, bssid_ = file_.split(".")[0].split("_")

            bssid = macify(bssid_)

            out["features"].append({
                "type": "Feature",
                "properties": {
                    "ssid": name,
                    "bssid": bssid
                },
                "geometry": {
                    "coordinates": [
                        j["location"]["lng"],
                        j["location"]["lat"]
                    ],
                    "type": "Point"
                }
            })
    
    with open(ns.output, "w") as outf:
        json.dump(out, outf)