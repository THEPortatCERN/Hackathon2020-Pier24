import numpy as np
import sklearn.cluster


def get_feature_vector(footprints):
    all_centroids = np.array([fp.centroid() for fp in footprints])
    all_areas = np.array([fp.area() for fp in footprints])
    return np.hstack((all_centroids, np.expand_dims(all_areas, 1)))


def cluster(footprints, eps=30, min_samples=8):
    features = get_feature_vector(footprints)
    labels = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples).fit_predict(features)

    clusters = []
    for _ in range(np.max(labels) + 2):
        clusters.append([])
    for idx, label in enumerate(labels):
        clusters[label + 1].append(footprints[idx])

    return clusters
