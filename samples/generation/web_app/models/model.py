import json

import numpy
import tensorflow as tf
from keras_preprocessing.image import img_to_array, load_img
from tensorflow.python.keras.applications import VGG16

# Load models and support
from tensorflow.python.keras.applications.imagenet_utils import preprocess_input
from tensorflow.python.keras.backend import clear_session
from tensorflow.python.keras.utils import get_file
from tensorflow.python.saved_model import tag_constants

CLASS_INDEX = None
CLASS_INDEX_PATH = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"


def get_predictions(predictions, top=5):
    global CLASS_INDEX
    if len(predictions.shape) != 2 or predictions.shape[1] != 1000:
        raise ValueError(
            f"`decode_predictions` expects a batch of predictions (i.e. a 2D array of shape (samples, "
            f"1000)). Found array with shape: {predictions.shape}"
        )
    if CLASS_INDEX is None:
        file_path = get_file(
            "imagenet_class_index.json", CLASS_INDEX_PATH, cache_subdir="models"
        )
        CLASS_INDEX = json.load(open(file_path))
    l = []
    for prediction in predictions:
        top_indices = prediction.argsort()[-top:][::-1]
        indexes = [tuple(CLASS_INDEX[str(i)]) + (prediction[i],) for i in top_indices]
        indexes.sort(key=lambda x: x[2], reverse=True)
        l.append(indexes)
    return l


def vgg_prepare_img_224(img_path):
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = numpy.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def get_predicted_categories(img_224) -> list:
    clear_session()
    image_net_model = VGG16(weights="imagenet")
    out = image_net_model.predict(img_224)
    topn = get_predictions(out, top=5)
    return topn


def prepare_img_size(img_path, size=299):
    img = load_img(img_path, target_size=(size, size))  # this is a PIL image
    x = img_to_array(img)  # this is a Numpy array with shape (3, 256, 256)
    x = x.reshape((1,) + x.shape) / 255
    return x


def predict(sess, model_graph, input_tensor):
    pass


def run_models(img_path, base_path, labels_path):
    labels = []

    with open(labels_path, "r") as f:
        for label in f.readlines():
            labels.append(label)

    try:
        img_224 = vgg_prepare_img_224(img_path)
        top_n_prediction = get_predicted_categories(img_224)

        zipped = [a for a in zip(*top_n_prediction[0])]
        vgg_predictions = {cat: prob for cat, prob in zip(zipped[1], zipped[2])}
    except:
        vgg_predictions = dict()

    try:
        image_in = prepare_img_size(img_path)
        clear_session()

        graph = tf.Graph()
        sess = tf.Session(graph=graph)
        tf.saved_model.loader.load(sess, [tag_constants.SERVING], base_path)

        category_result = predict(sess, model_graph=graph, input_tensor=image_in)

        dlp_predictions = {k: v for v, k in zip(category_result, labels)}
    except Exception as e:
        dlp_predictions = dict()
        print(f"failed dlp_prediction {e}")

    message = "Assessment complete!"

    results = {"dlp_predictions": dlp_predictions, "vgg_predictions": vgg_predictions}

    return {"results": results, "message": message}
