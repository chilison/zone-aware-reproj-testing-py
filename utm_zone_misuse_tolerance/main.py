import math
import matplotlib.pyplot as plt
from pyproj import Proj, Geod
from geopy.distance import geodesic


# Chose not to decompose, as it's simple enough and serves a one-time visualization experiment

longitudes = [36.00001, 36.0001, 36.001, 36.01, 36.05, 36.1]
utm36 = Proj(proj="utm", zone=36, datum="WGS84")
geod = Geod(ellps="WGS84")

latitudes = list(range(0, 86, 1))
abs_differences = {long: [] for long in longitudes}
rel_differences = {long: [] for long in longitudes}

for lat in latitudes:
    for long in longitudes:
        x1, y1 = utm36(36, lat)
        x2, y2 = utm36(long, lat)

        p1 = (lat, 36)
        p2 = (lat, long)

        utm_dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        geod_dist = geodesic(p1, p2).meters

        abs_diff = abs(utm_dist - geod_dist)
        rel_diff = abs_diff / geod_dist * 100

        abs_differences[long].append(abs_diff)
        rel_differences[long].append(rel_diff)

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

for long, diffs in abs_differences.items():
    axs[0].plot(latitudes, diffs, marker="o", label=f"{long}°")
axs[0].set_title("Absolute Error (m)")
axs[0].set_xlabel("Latitude")
axs[0].set_ylabel("Error (m)")
axs[0].grid()
axs[0].legend()

for long, diffs in rel_differences.items():
    axs[1].plot(latitudes, diffs, marker="x", label=f"{long}°")
axs[1].set_title("Relative error (%)")
axs[1].set_xlabel("Latitude")
axs[1].set_ylabel("Error (%)")
axs[1].grid()
axs[1].legend()

axs[0].tick_params(axis='both', length=2, width=0.2)
axs[1].tick_params(axis='both', length=2, width=0.2)

plt.tight_layout()
plt.show()
