from pyproj import Proj, Transformer, Geod

geod = Geod(ellps="WGS84")


def latlon_to_utm(lon, lat):
    """
    Converts longitude and latitude to x, y, UTM zone number and hemisphere.

    Args:
        lon (float): longitude.
        lat (float): latitude.

    Returns:
        x (float): x coordinate.
        y (float): y coordinate.
        zone (int): UTM zone number.
        hemisphere (string): hemisphere.
    """
    zone = int((lon + 180) / 6) + 1
    hemisphere = "north" if lat >= 0 else "south"
    utm_proj = Proj(proj="utm", zone=zone, south=(lat < 0), ellps="WGS84")
    x, y = Transformer.from_proj("epsg:4326", utm_proj).transform(lon, lat)
    return x, y, zone, hemisphere


def utm_to_latlon(x, y, zone, hemisphere):
    """
    Converts UTM coordinates into longitude and latitude.

    Args:
        x (float): x coordinate.
        y (float): y coordinate.
        zone (int): UTM zone number.
        hemisphere (string): hemisphere.

    Returns:
        lon (float): longitude.
        lat (float): latitude.
    """
    utm_proj = Proj(proj="utm", zone=zone, south=(hemisphere == "south"), ellps="WGS84")
    lon, lat = Transformer.from_proj(utm_proj, "epsg:4326").transform(x, y)
    return lon, lat


def latlon_to_eqdc(lon, lat, lat_min, lat_max, lon_center):
    """
    Converts longitude and latitude to x, y in Equidistant conic projection.

    Args:
        lon (float): longitude.
        lat (float): latitude.

    Returns:
        x (float): x coordinate.
        y (float): y coordinate.
    """
    eqdc_proj = Proj(proj="eqdc", lat_1=lat_min, lat_2=lat_max, lon_0=lon_center, datum="WGS84")
    return eqdc_proj(lon, lat)


def latlon_to_tmerc(lon, lat, lat_center, lon_center):
    """
    Converts longitude and latitude to x, y in Transverse Mercator projection.

    Args:
        lon (float): longitude.
        lat (float): latitude.

    Returns:
        x (float): x coordinate.
        y (float): y coordinate.
    """
    tmerc_proj = Proj(proj="tmerc", lat_0=lat_center, lon_0=lon_center, datum="WGS84")
    return tmerc_proj(lon, lat)
