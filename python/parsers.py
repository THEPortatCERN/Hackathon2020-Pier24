import numpy as np
import pyproj
import scipy.spatial
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import shapefile
from pathlib import Path
import fiona
from shapely.geometry import mapping


class LabelPoint:
    def __init__(self, point: np.ndarray, label: str, category: str):
        self.point = point
        self.label = label
        self.category = category


class ZambiaFootprint:
    def __init__(self, polygon: Polygon, label: str = "", category: str = ""):
        self.polygon = polygon
        self.label = label
        self.category = category

    def centroid(self):
        return np.array([self.polygon.centroid.x, self.polygon.centroid.y])

    def area(self):
        return self.polygon.area

    def points(self):
        return np.vstack((np.array(self.polygon.boundary.coords.xy[0]), np.array(self.polygon.boundary.coords.xy[1]))).T

    def is_residential(self):
        return self.category in ["cabin", "Residential", "farm", "residential", "apartments"]

    def is_unknown(self):
        return self.category == "" or self.category in ["hut", "house", "detached", "building", "Building",
                                                        "commercial;residenti", "guest_house",
                                                        "dormitory", "unknown"]

    def is_not_residential(self):
        return not (self.is_residential() or self.is_unknown())


def parse_polygon_shp(path: str):
    shape = shapefile.Reader(path)
    polygons = []
    for feature in shape.shapeRecords():
        polygon = Polygon(feature.shape.points)
        if not polygon.is_empty:
            polygons.append(polygon)

    return polygons


def parse_point_shp(path: str, crs_wkt):
    shape = shapefile.Reader(path)
    points = []

    proj_label_to_footprint_crs = pyproj.proj.Proj(crs_wkt)
    for feature in shape.shapeRecords():
        point = feature.shape.points[0]
        point_fp_crs = proj_label_to_footprint_crs(point[0], point[1])
        points.append(LabelPoint(np.array(point_fp_crs), feature.record[4], feature.record[5]))
    return points


def associate_footprint_polygons_and_labels(footprints, label_points):
    centroids_fp = np.array([[fp.centroid.x, fp.centroid.y] for fp in footprints if not fp.is_empty])

    kdTree_footprints = scipy.spatial.cKDTree(centroids_fp)

    labeled_footprints = [ZambiaFootprint(footprint) for footprint in footprints]
    for label_point in label_points:
        neighbouring_footprint_idxs = kdTree_footprints.query_ball_point(label_point.point, r=20, p=2.0, eps=1)
        for footprint_idx in neighbouring_footprint_idxs:
            shpPolygon = footprints[footprint_idx]
            shpPoint = Point(label_point.point)
            if shpPolygon.contains(shpPoint):
                labeled_footprints[footprint_idx].label = label_point.label
                labeled_footprints[footprint_idx].category = label_point.category
                continue

    return labeled_footprints


def get_coord_sys(path):
    prj_path = Path(path).with_suffix(".prj")
    with open(str(prj_path)) as f:
        wkt_str = f.readline()
    return wkt_str


def get_zambia_footprints(path_footprints: str, path_labels: str):
    """Given the paths to the shapefiles, returns a list of `ZambiaFootprint`, and the coordinate system definition"""
    footprint_polygons = parse_polygon_shp(path_footprints)
    footprints_crs = get_coord_sys(path_footprints)
    labels = parse_point_shp(path_labels, footprints_crs)

    return associate_footprint_polygons_and_labels(footprint_polygons, labels), footprints_crs


def write_to_shapefile(path: str, footprints: ZambiaFootprint, crs: str):
    """Writes the provided ZambiaFootprints to a shapefile, with the given coordinatesystem"""
    schema = {"geometry": "Polygon", "properties": {"label": "str", "category": "str"}}
    with fiona.open(path, 'w', crs=crs, schema=schema, driver='ESRI Shapefile') as output:
        for footprint in footprints:
            output.write({"geometry": mapping(footprint.polygon),
                          "properties": {"label": footprint.label, "category": footprint.category}})
