import datetime
import json
import urllib.request

with open("games.json") as f:
    games = json.load(f)

universe_ids = ",".join(str(v) for v in games.values())
url = f"https://games.roblox.com/v1/games?universeIds={universe_ids}"
with urllib.request.urlopen(url) as resp:
    data = json.load(resp)["data"]

by_id = {g["id"]: g for g in data}

stats = {
    "updatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "games": {
        slug: {
            "universeId": uid,
            "playing": by_id[uid]["playing"],
            "visits": by_id[uid]["visits"],
        }
        for slug, uid in games.items()
    },
}

with open("stats.json", "w") as f:
    json.dump(stats, f, indent=2)
    f.write("\n")
