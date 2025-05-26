# zone-aware-reproj-testing-py

This repository contains code for reproducing experiments conducted for [zone-aware-reproj-cpp](https://github.com/chilison/zone-aware-reproj-cpp) library. The experiments include:

1. **UTM Zone Misuse Tolerance**  
   Testing how far you can go outside the correct UTM zone before errors become too large.

2. **Projection Selection Based on Two Points**  
   Choosing the best projection based on distance between two points and adjusting the projection automatically.

3. **Projection Selection with Fixed Parameters**  
   Evaluating projections with fixed settings using test points near the projection center.

4. **Modeling**  
   Simulating how the full projection system works to test the logic and finalize the projection selection.

5. **GeoTIFF preparation**
   Preparing GeoTIFF testing data by automatically splitting and reprojecting to the according UTM zone.  