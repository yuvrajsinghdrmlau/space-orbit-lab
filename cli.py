import argparse
import json

from model import simulate

parser = argparse.ArgumentParser(description="Run a two-body orbit simulation.")
parser.add_argument("--body", choices=["Earth", "Mars"], default="Mars")
parser.add_argument("--altitude", type=float, default=400)
parser.add_argument("--duration", type=float, default=120)
parser.add_argument("--inclination", type=float, default=35)
parser.add_argument("--speed-factor", type=float, default=1)
args = parser.parse_args()
print(json.dumps(simulate(args.body, args.altitude, args.duration, args.inclination, args.speed_factor), indent=2))
