from python.parsers import get_zambia_footprints, write_to_shapefile
from python.clustering import build_classifier, predict

footprints_path = "MY_PATH_TO_FOOTPRINT"
labels_path = "MY_PATH_TO_FOOTPRINT"
output_shapefile_residential = "RESIDENTIAL_PATH"
output_shapefile_not_residential = "NOT_RESIDENTIAL_PATH"

footprints, coordinate_sys = get_zambia_footprints(footprints_path, labels_path)

classifier, score = build_classifier(footprints)
print(f"The classifier score is {score}")

labels = predict(footprints, classifier)

residential = []
not_residential = []
for idx, label in enumerate(labels):
    if label == 1:
        residential.append(footprints[idx])
    else:
        not_residential.append(footprints[idx])

write_to_shapefile(output_shapefile_residential, residential, coordinate_sys)
write_to_shapefile(output_shapefile_not_residential, not_residential, coordinate_sys)