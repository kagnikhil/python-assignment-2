
import json
from collections import defaultdict


def read_records(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)
                device = record["device_id"]
                temp = float(record["temperature_c"])
                humidity = float(record["humidity"])

                if not device or not 0 <= humidity <= 100:
                    raise ValueError

                yield device, temp, humidity

            except (ValueError, TypeError, KeyError, json.JSONDecodeError):
                yield None


def process_file(path):
    stats = defaultdict(lambda: {
        "count": 0,
        "min": float("inf"),
        "max": float("-inf"),
        "total": 0.0,
        "corrupted": 0
    })

    for record in read_records(path):
        if record is None:
            continue

        device, temp, humidity = record

        if not -100 <= temp <= 100:
            stats[device]["corrupted"] += 1
            continue

        s = stats[device]
        s["count"] += 1
        s["min"] = min(s["min"], temp)
        s["max"] = max(s["max"], temp)
        s["total"] += temp

    return stats


def main():
    path = input("Enter JSONL file path: ").strip()

    try:
        stats = process_file(path)

        for device in sorted(stats):
            s = stats[device]

            if s["count"]:
                average = s["total"] / s["count"]
                print(
                    f"{device} count={s['count']} "
                    f"min={s['min']:g} max={s['max']:g} "
                    f"avg={average:.2f} corrupted={s['corrupted']}"
                )
            else:
                print(f"{device} count=0 corrupted={s['corrupted']}")

    except OSError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
