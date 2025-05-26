# Experiment: UTM Zone Misuse Tolerance

## Objective

Testing how far you can go outside the correct UTM zone before errors become too large.

## How It Works 🧐

For different latitudes, the script shifts a second point by varying degrees of longitude—meaning the second point often lies in a different UTM zone. However, it projects this second point using the UTM projection rules of the original (first) zone. Then it calculates the distance between the two points in this projected coordinate system and compares it to the true geodesic distance on the Earth's surface. This comparison reveals the absolute and relative errors introduced by applying the UTM projection outside its correct zone.

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
