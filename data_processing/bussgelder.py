import argparse
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm, trange


def load_raw_data(fname, verkehrstyp):
    raw = pd.read_csv(fname)
    if "Tatort 2" in raw:
        raw["Tatort"] = stehend["Tatort 2"]
        raw = stehend.drop(["Tatort 2"], axis=1)
    raw["Verkehrstyp"] = verkehrstyp
    raw["lat"] = np.nan
    raw["lon"] = np.nan
    raw["accuracy"] = ""
    return raw


def set_coordinates(df, out_fname, nominatim_url="http://localhost:7070"):
    streets = df[df.lat.isna()]["Tatort"].unique()
    ignores = [
        "ggü. Haus-Nr.",
        "vor Haus-Nr.",
        "neben Haus-Nr.",
        "zwischen Haus-Nr.",
        "Stichstraße",
    ]

    print("Straße ohne Hausnummer")
    street_names = set(map(lambda x: x.split(" ")[0] if isinstance(x, str) else None , streets))
    for i, street in enumerate(tqdm(street_names)):
        if not street:
            continue
        query = street.strip()
        resp = requests.get(f"{nominatim_url}/search/?city=Aachen&street={query}&format=json")
        data = resp.json()
        if len(data) > 0:
            point = data[0]
            df.loc[df["Tatort"].str.split(" ").str[0] == query, "lat"] = point.get("lat", np.nan)
            df.loc[df["Tatort"].str.split(" ").str[0] == query, "lon"] = point.get("lon", np.nan)
            df.loc[df["Tatort"].str.split(" ").str[0] == query, "accuracy"] = "street"
        if i % 1000 == 0:
            df.to_csv(out_fname)
    df.to_csv(out_fname)

    print("Straße + Hausnummer")
    for i, street in enumerate(tqdm(streets)):
        query = street
        try:
            for ignore in ignores:
                query = query.replace(ignore, "")
        except:
            continue

        resp = requests.get(f"{nominatim_url}/search/?city=Aachen&street={query}&format=json")
        data = resp.json()
        if len(data) > 0:
            point = data[0]
            df.loc[df["Tatort"] == street, "lat"] = point.get("lat", np.nan)
            df.loc[df["Tatort"] == street, "lon"] = point.get("lon", np.nan)
            df.loc[df["Tatort"] == street, "accuracy"] = "exact"
        if i % 1000 == 0:
            df.to_csv(out_fname)

    df.to_csv(out_fname)

def main():
    parser = argparse.ArgumentParser(
            description="Skript um Aachen Bussgeld Daten um GPS Koordinaten zu erweitern und zu vereinheitlichen")
    parser.add_argument("input", metavar="i", type=str, help="Pfad zur Original CSV")
    parser.add_argument("output", metavar="o", type=str, help="Ausgabe Pfad")
    parser.add_argument("type", metavar="t", type=str, help="Verkehrstyp (z.B. stehend oder fliessend)")
    parser.add_argument("--nominatim", type=str, help="URL des Nominatim Servers", default="http://localhost:7070")

    args = parser.parse_args()
    df = load_raw_data(args.input, args.type)
    set_coordinates(df, args.output, args.nominatim)
    pass

if __name__ == "__main__":
    main()
