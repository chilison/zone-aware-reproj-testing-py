import random
import math
from .projection import geod, latlon_to_utm, utm_to_latlon, latlon_to_eqdc, latlon_to_tmerc


def generate_latlon_points(center_lat, center_lon, count=1, min_dist=1000, max_dist=10000):
    """
    Generates points (their latitudes and longitudes) in a chain using the solution to the direct geodesic problem. A random azimuth angle is chosen within a π range to avoid movement in opposite directions, and a segment of random length from 1 km to 10 km is used by default.

    Args:
        center_lat (float): initial latitude.
        center_lon (float): initial longitude.
        count (int): number of points in a current batch.
        min_dist (float): minimal length of a distance.
        max_dist (float): maximal length of a distance.

    Returns:
        points (list[]): generated batch of points.
    """
    points = []
    for _ in range(count):
        angle = random.uniform(0, math.pi)
        distance = random.uniform(min_dist, max_dist)
        lon, lat, _ = geod.fwd(center_lon, center_lat, math.degrees(angle), distance)
        x, y, zone, hemisphere = latlon_to_utm(lon, lat)
        points.append({
            "utm_x": x,
            "utm_y": y,
            "utm_zone": zone,
            "utm_hemisphere": hemisphere,
            "original_lat": None,
            "original_lon": None
        })
        center_lon = lon
        center_lat = lat
    return points


def update_all_points(points):
    """
    Fills in missing coordinate fields if necessary, determines projection parameters based on input data, and updates the dataset

    Args:
        points (list[]): list of generated points.
    """
    for p in points:
        if p["original_lat"] is None or p["original_lon"] is None:
            lon, lat = utm_to_latlon(p["utm_x"], p["utm_y"], p["utm_zone"], p["utm_hemisphere"])
            p["original_lat"] = lat
            p["original_lon"] = lon

    lat_min = min(p["original_lat"] for p in points)
    lat_max = max(p["original_lat"] for p in points)
    lat_avg = sum(p["original_lat"] for p in points) / len(points)
    lon_avg = sum(p["original_lon"] for p in points) / len(points)

    for p in points:
        eqdc_x, eqdc_y = latlon_to_eqdc(p["original_lon"], p["original_lat"], lat_min, lat_max, lon_avg)
        tmerc_x, tmerc_y = latlon_to_tmerc(p["original_lon"], p["original_lat"], lat_avg, lon_avg)
        p.update({
            "eqdc_x": eqdc_x,
            "eqdc_y": eqdc_y,
            "tmerc_x": tmerc_x,
            "tmerc_y": tmerc_y
        })
