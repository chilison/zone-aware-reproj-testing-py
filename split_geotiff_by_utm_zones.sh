#!/bin/bash

INPUT_TIFF="input.tiff"
OUT_DIR="split_zones"
mkdir -p "$OUT_DIR"
export LC_NUMERIC=C

json=$(gdalinfo -json "$INPUT_TIFF")

MINLON=$(echo "$json" | jq '.cornerCoordinates.upperLeft[0]')
MAXLON=$(echo "$json" | jq '.cornerCoordinates.upperRight[0]')
MAXLAT=$(echo "$json" | jq '.cornerCoordinates.upperLeft[1]')
MINLAT=$(echo "$json" | jq '.cornerCoordinates.lowerRight[1]')

echo "GeoTIFF: [$MINLON,$MAXLON] by longitude, [$MINLAT,$MAXLAT] by latitude"


UTM_ZONE_MIN=$(( (180 + $(printf "%.0f" "$MINLON")) / 6 + 1 ))
UTM_ZONE_MAX=$(( (180 + $(printf "%.0f" "$MAXLON")) / 6 + 1 ))

echo "📐 UTM zones: $UTM_ZONE_MIN → $UTM_ZONE_MAX"

for ZONE in $(seq "$UTM_ZONE_MIN" "$UTM_ZONE_MAX"); do
    EPSG=$(( 32600 + ZONE ))

   ZONELON_MIN=$(echo "($ZONE - 1) * 6 - 180" | bc)
    ZONELON_MAX=$(echo "$ZONELON_MIN + 6" | bc)

    CROP_MINLON=$(echo "$ZONELON_MIN > $MINLON" | bc -l | grep -q 1 && echo "$ZONELON_MIN" || echo "$MINLON")
    CROP_MAXLON=$(echo "$ZONELON_MAX < $MAXLON" | bc -l | grep -q 1 && echo "$ZONELON_MAX" || echo "$MAXLON")

    echo "▶️ Split by zone $ZONE:"
    echo "    xmin=$CROP_MINLON, ymin=$MINLAT, xmax=$CROP_MAXLON, ymax=$MAXLAT"

    WIDTH=$(echo "$CROP_MAXLON > $CROP_MINLON" | bc -l)
    HEIGHT=$(echo "$MAXLAT > $MINLAT" | bc -l)

    if [[ "$WIDTH" -eq 1 && "$HEIGHT" -eq 1 ]]; then
        TMP_TIF="$OUT_DIR/tmp_zone_${ZONE}.tif"

        gdalwarp -overwrite -s_srs EPSG:4326 -t_srs EPSG:4326 \
          -te "$CROP_MINLON" "$MINLAT" "$CROP_MAXLON" "$MAXLAT" \
          "$INPUT_TIFF" "$TMP_TIF"

        gdalwarp -overwrite -s_srs EPSG:4326 -t_srs EPSG:$EPSG \
          "$TMP_TIF" "$OUT_DIR/utm_zone_${ZONE}.tif"

        rm "$TMP_TIF"

    else
        echo "There's no such zone!!!"
    fi
done
