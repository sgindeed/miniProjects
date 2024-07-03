import geemap
import ee

ee.Initialize()

aoi = ee.Geometry.Polygon([[
    [88.125107, 22.8088712],
    [87.9987643, 22.6289945],
    [88.1663058, 22.166829],
    [88.7540743, 22.2558261],
    [88.7375948, 22.75316],
    [88.125107, 22.8088712]
]])

Map = geemap.Map(center=[88.3629, 22.5744], zoom=12)
Map.addLayer(aoi, {}, 'AOI')

modis_lst = ee.ImageCollection("MODIS/061/MOD11A2")\
.select('LST_Day_1km')\
.filterDate('2024-06-01', '2024-06-05').mean().clip(aoi)
Map.setCenter(88.3629, 22.5744, 8)

sentinel_ndvi = ee.ImageCollection('COPERNICUS/S2_HARMONIZED').filterDate('2024-06-01', '2024-06-05').filterBounds(aoi).map(lambda image: image.normalizedDifference(['B8', 'B4']).rename('NDVI')).mean().clip(aoi)
Map.setCenter(88.3629, 22.5744, 8)

Map.addLayer(modis_lst, {'min': 13000, 'max': 16500, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}, 'MODIS LST')
Map.addLayer(sentinel_ndvi, {'min': 0, 'max': 1, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}, 'Sentinel-2 NDVI')

Map

def split_aoi(aoi, n):
    coords = aoi.coordinates().get(0).getInfo()
    min_lon = min([c[0] for c in coords])
    max_lon = max([c[0] for c in coords])
    min_lat = min([c[1] for c in coords])
    max_lat = max([c[1] for c in coords])
    
    lon_step = (max_lon - min_lon) / n
    lat_step = (max_lat - min_lat) / n

    regions = []
    for i in range(n):
        for j in range(n):
            region = ee.Geometry.Rectangle(
                [min_lon + i * lon_step, min_lat + j * lat_step, min_lon + (i + 1) * lon_step, min_lat + (j + 1) * lat_step]
            )
            regions.append(region)
    return regions

def export_small_regions(image, regions, prefix, scale):
    paths = []
    for idx, region in enumerate(regions):
        path = f'{prefix}_{idx}.tif'
        geemap.ee_export_image(image, filename=path, scale=scale, region=region, file_per_band=False)
        paths.append(path)
    return paths

def collect_and_download_data():
    modis_lst = ee.ImageCollection("MODIS/061/MOD11A2")\
    .select('LST_Day_1km')\
    .filterDate('2024-06-01', '2024-06-05').mean().clip(aoi)

    sentinel_ndvi = ee.ImageCollection('COPERNICUS/S2_HARMONIZED').filterDate('2024-06-01', '2024-06-05').filterBounds(aoi).map(lambda image: image.normalizedDifference(['B8', 'B4']).rename('NDVI')).mean().clip(aoi)

    regions = split_aoi(aoi, 3)  # Split the AOI into 3x3 smaller regions

    modis_lst_paths = export_small_regions(modis_lst, regions, 'MODIS_LST', 1000)
    sentinel_ndvi_paths = export_small_regions(sentinel_ndvi, regions, 'Sentinel_NDVI', 10)

    return modis_lst_paths, sentinel_ndvi_paths

lst_paths, ndvi_paths = collect_and_download_data()


import rasterio
import numpy as np
import pandas as pd

def preprocess_raster(path):
    with rasterio.open(path) as src:
        return src.read(1), src.transform

lst_data_list = [preprocess_raster(path)[0] for path in lst_paths]
ndvi_data_list = [preprocess_raster(path)[0] for path in ndvi_paths]

min_shape = (min([data.shape[0] for data in lst_data_list]),
             min([data.shape[1] for data in lst_data_list]))

lst_data_list = [data[:min_shape[0], :min_shape[1]] for data in lst_data_list]
ndvi_data_list = [data[:min_shape[0], :min_shape[1]] for data in ndvi_data_list]

lst_data = np.concatenate(lst_data_list, axis=0)
ndvi_data = np.concatenate(ndvi_data_list, axis=0)

lst_flat = lst_data.flatten()
ndvi_flat = ndvi_data.flatten()

df = pd.DataFrame({
    'LST': lst_flat,
    'NDVI': ndvi_flat
})

df = df.dropna()

df.head(500)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

X = df[['NDVI']]
y = df['LST']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

df['LST_Predicted'] = model.predict(df[['NDVI']])

lst_predicted = df['LST_Predicted'].values.reshape(lst_data.shape)

with rasterio.open('Predicted_LST.tif', 'w', driver='GTiff', height=lst_predicted.shape[0],
                   width=lst_predicted.shape[1], count=1, dtype=lst_predicted.dtype, 
                   crs='EPSG:4326', transform=preprocess_raster(lst_paths[0])[1]) as dst:
    dst.write(lst_predicted, 1)

from sklearn.metrics import mean_absolute_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mae

r2 = r2_score(y_test, y_pred)
r2

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.imshow(lst_predicted, cmap='viridis')
plt.colorbar(label='Predicted LST (K)')
plt.title('Predicted Land Surface Temperature')
plt.show()
