# image_classifier.py
import cv2
import numpy as np
from keras.models import load_model


def image_classifier(image, model_path, labels_path):
    """Classify the given image using a pre-trained model."""
    np.set_printoptions(suppress=True)

    model = load_model(model_path, compile=False)

    class_names = open(labels_path, "r").readlines()

    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    cv2.imshow("Image", image)

    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    image = (image / 127.5) - 1

    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class:", class_name[2:])
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    return class_name[2:]


if __name__ == "__main__":
    pass
