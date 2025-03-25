import io
import tempfile
from fastapi import HTTPException
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.layers import InputLayer as BaseInputLayer

labels = ['Benign cases', 'Malignant cases', 'Normal cases']

def preprocess_image(image_bytes: bytes, target_size=(224, 224)):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(target_size)
        img_array = np.array(image)
        if img_array.shape[-1] == 4:
            img_array = img_array[..., :3]
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Xử lý ảnh thất bại: {e}")

def load_model_from_file(file_path: str):
    try:
        class CustomInputLayer(BaseInputLayer):
            def __init__(self, **kwargs):
                if 'batch_shape' in kwargs:
                    batch_shape = kwargs.pop('batch_shape')
                    if 'shape' not in kwargs:
                        kwargs['shape'] = batch_shape[1:]
                super().__init__(**kwargs)
        custom_objects = {'InputLayer': CustomInputLayer}
        model = tf.keras.models.load_model(file_path, compile=False, custom_objects=custom_objects)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể load model từ file: {e}")

def load_model_from_bytes(model_bytes: bytes):
    try:
        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
            tmp.write(model_bytes)
            tmp.flush()
        class CustomInputLayer(BaseInputLayer):
            def __init__(self, **kwargs):
                if 'batch_shape' in kwargs:
                    batch_shape = kwargs.pop('batch_shape')
                    if 'shape' not in kwargs:
                        kwargs['shape'] = batch_shape[1:]
                super().__init__(**kwargs)
        custom_objects = {'InputLayer': CustomInputLayer}
        model = tf.keras.models.load_model(tmp.name, compile=False, custom_objects=custom_objects)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể load model: {e}")

def predict_diagnosis(model, image_bytes: bytes):
    img_array = preprocess_image(image_bytes)
    predictions = model.predict(img_array)
    predicted_index = int(np.argmax(predictions[0]))
    predicted_label = labels[predicted_index]
    confidence = float(predictions[0][predicted_index])
    return {
        "predicted_label": predicted_label,
        "confidence": confidence,
    }
