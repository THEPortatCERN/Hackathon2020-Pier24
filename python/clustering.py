import numpy as np
import sklearn.cluster
import scipy.spatial
from sklearn.ensemble import GradientBoostingClassifier


def get_feature_vector(footprints, footprints_subset, radius=20):
    centroids_fp = np.array([fp.centroid() for fp in footprints])
    kdTree_footprints = scipy.spatial.cKDTree(centroids_fp)

    areas = []
    hull_areas = []
    n_neighbours = []
    neighbour_avg_area = []
    lengths = []
    for fp in footprints_subset:
        neighbouring_footprint_idxs = kdTree_footprints.query_ball_point(fp.centroid(), r=radius, p=2.0,
                                                                         return_sorted=True)[1:]
        neighbour_areas_sum = 0
        for idx in neighbouring_footprint_idxs:
            neighbour = footprints[idx]
            neighbour_areas_sum += neighbour.area()

        if len(neighbouring_footprint_idxs) == 0:
            neighbour_avg_area.append(0.0)
        else:
            neighbour_avg_area.append(neighbour_areas_sum / len(neighbouring_footprint_idxs))
        n_neighbours.append(len(neighbouring_footprint_idxs))
        areas.append(fp.area())
        hull_areas.append(fp.polygon.convex_hull.area)
        lengths.append(fp.polygon.length)

    return np.vstack((areas, hull_areas, n_neighbours, neighbour_avg_area, lengths)).T


def cluster(footprints, eps=30, min_samples=8):
    features = get_feature_vector(footprints)
    labels = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples).fit_predict(features)

    clusters = []
    for _ in range(np.max(labels) + 2):
        clusters.append([])
    for idx, label in enumerate(labels):
        clusters[label + 1].append(footprints[idx])

    return clusters


def build_classifier(footprints):
    labeled_data = np.array([fp for fp in footprints if not fp.is_unknown()])
    features = get_feature_vector(footprints, labeled_data)
    rng = np.random.RandomState(seed=1)
    train_idxs = rng.choice(list(range(len(labeled_data))), size=int(0.8 * len(labeled_data)))
    test_idxs = list(set(list(range(len(labeled_data)))).difference(set(train_idxs)))

    x_train = features[train_idxs]
    x_test = features[test_idxs]

    y_train = np.array([int(labeled_data[idx].is_residential()) for idx in train_idxs])
    y_test = np.array([int(labeled_data[idx].is_residential()) for idx in test_idxs])

    classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0)
    classifier.fit(x_train, y_train)
    score = classifier.score(x_test, y_test)

    return classifier, score


def predict(footprints, classifier):
    features = get_feature_vector(footprints, footprints)
    return classifier.predict(features)
