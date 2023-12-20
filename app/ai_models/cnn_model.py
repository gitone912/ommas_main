import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import numpy as np

def train_and_save_model(train_data_dir, model_save_path):
    # Load pre-trained model without top layers
    base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    # Add new layers
    model = models.Sequential()
    model.add(base_model)
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))

    # Freeze pre-trained layers
    for layer in base_model.layers:
        layer.trainable = False

    # Data Augmentation
    datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

    # Confirm the existence of images in the directory
    print("Number of images:", len(datagen.flow_from_directory(train_data_dir, target_size=(224, 224), batch_size=32, class_mode='binary').filenames))

    # Compile the model
    model.compile(optimizer=optimizers.Adam(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit_generator(datagen.flow_from_directory(train_data_dir, target_size=(224, 224), batch_size=32, class_mode='binary'), epochs=40)

    # Save the model
    model.save(model_save_path)

def predict_image(img_path):
    # Load the trained model
    model = tf.keras.models.load_model('/Users/pranaymishra/Desktop/sih1429/ommas_main/app/ai_models/tile_detection_model.h5')

    # Load and preprocess a new image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.

    # Make predictions
    predictions = model.predict(img_array)

    # Print the prediction (1 if tile is present, 0 otherwise)
    print(predictions)
    if predictions[0][0] > 0.5:
        return 'DATA SATISFACTORY ( TILE DETECTED )'
    else:
        return 'DATA UNSATISFACTORY ( NEEDS IMPROVEMENT )'


# train_and_save_model('/Users/pranaymishra/Desktop/OMMAS_Modeling/images', 'tile_detection_model.h5')
# predict_image('tile_detection_model.h5', '/Users/pranaymishra/Desktop/OMMAS_Modeling/lovepik-forest-road-highway-picture_501669994.jpg')
# predict_image('tile_detection_model.h5', '/Users/pranaymishra/Desktop/OMMAS_Modeling/Screenshot 2023-12-16 at 12.16.50 AM.png')
