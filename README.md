# Hackathon2020-Pier24

> Content for submission.

# Index

- [Problem Workflow](#problem-workflow)
- [Datasets](#datasets)
- [Tasks](#tasks)
- [References](#references)
## Problem-workflow

<img src="https://github.com/THEPortatCERN/Hackathon2020-Pier24/tree/master/resources/workflow.png" alt="" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" height="400" />


## Datasets

### [rio](https://spacenet.ai/rio-de-janeiro/)

> __Rio de Janeiro (Brazil)__ satellite imaging dataset for [__SpaceNet 1: Building Detection v1__](https://spacenet.ai/spacenet-buildings-dataset-v1/) challenge.

```
train:   3,8 band satellite images (raster) & building-footprints (vector) for Rio-de-Janeiro (2784 sq KM) collected by WorldView-2
  mosaic: 3 band mosaic of dataset & building-footprints
test:    3,8 band satellite images (raster) for Rio-de-Janeiro (2784 sq KM) collected by WorldView-2
labels:  Compressed 3,8 band 200m x 200m tiles with associated building foot print labels
landuse: Categorized land regions (shp/geojson) [22946 features].
```

- landuse data has 18 regional classes.
    ```powershell
    $regex='"fclass": "(\w+)"'
    $classes = Select-String -Path '.\landuse.geojson' -Pattern $regex -AllMatches | forEach {$_.matches.groups[0]} | forEach {$_.Value -replace $regex,'$1'} | Sort-Object | Get-Unique

    allotments
    cemetery
    commercial
    farm
    forest
    grass
    heath
    industrial
    meadow
    military
    nature_reserve
    orchard
    park
    quarry
    recreation_ground
    residential
    retail
    scrub
    ```

### __[lusaka]()__ <br>

> __Lusaka (Zambia)__ satellite imaging dataset.

- [lusaka-dem](https://opendata.rcmrd.org/datasets/zambia-srtm-dem-30-metres) <br>
    30m resolution DEM raster dataset for Zambia region.
## Tasks
- [here](https://github.com/THEPortatCERN/Hackathon2020-Pier24/projects/1) <br>

## Resources

- [GitHub: Recipies](docs/github.md)

# References
- [UN Habitat](https://unhabitat.org/sites/default/files/documents/2019-07/zambia_urban_housing_sector_profile.pdf)
