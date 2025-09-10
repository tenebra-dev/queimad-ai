import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import requests
from io import BytesIO
from PIL import Image
import kagglehub
import os

print("🔥 FIRE DETECTION - Training a Real Model")
print("=" * 50)

# Download dataset
print("Downloading dataset...")
dataset_path = kagglehub.dataset_download("alik05/forest-fire-dataset")
base_path = os.path.join(dataset_path, "Forest Fire Dataset")
train_path = os.path.join(base_path, "Training")

print(f"Dataset path: {train_path}")

# Quick training setup
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

def train_quick_model():
    """Train a quick model with the fire dataset"""
    
    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    # Training data
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    
    # Validation data
    val_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )
    
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {val_generator.samples}")
    print(f"Classes found: {list(train_generator.class_indices.keys())}")
    
    # Create model
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    base_model.trainable = False  # Freeze base model
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(2, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n🤖 Model Architecture:")
    model.summary()
    
    # Train with early stopping to prevent overfitting
    print("\n🏋️ Starting training with early stopping...")
    
    # Early stopping callback
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,  # Stop if no improvement for 5 epochs
        restore_best_weights=True,
        verbose=1
    )
    
    # Model checkpoint to save best model
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        'models/checkpoints/best_fire_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    
    history = model.fit(
        train_generator,
        epochs=50,  # Higher limit, but early stopping will control
        validation_data=val_generator,
        callbacks=[early_stopping, checkpoint],
        verbose=1
    )
    
    # Save the model with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f'models/trained/fire_detection_model_{timestamp}.h5'
    model.save(model_filename)
    print(f"\n✅ Model saved as: {model_filename}")
    
    # Also save as the latest version for easy testing
    latest_model_path = 'models/trained/trained_fire_detection_model.h5'
    model.save(latest_model_path)
    print(f"✅ Latest model saved as: {latest_model_path}")
    
    # Plot training results
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('models/trained/quick_training_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    return model, history

def test_trained_model(model):
    """Test the trained model with some samples"""
    
    print("\n🧪 Testing the trained model...")
    
    # Test with a few images
    fire_path = os.path.join(train_path, "fire")
    nofire_path = os.path.join(train_path, "nofire")
    
    fire_files = [f for f in os.listdir(fire_path) if f.endswith('.jpg')][:3]
    nofire_files = [f for f in os.listdir(nofire_path) if f.endswith('.jpg')][:3]
    
    results = []
    
    # Test fire images
    print("\n🔥 Testing FIRE images:")
    for filename in fire_files:
        img_path = os.path.join(fire_path, filename)
        img = Image.open(img_path).convert("RGB")
        img_resized = img.resize((224, 224))
        
        img_array = image.img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        preds = model.predict(img_array, verbose=0)[0]
        class_idx = np.argmax(preds)
        classes = ["Fire", "No Fire"]
        label = classes[class_idx]
        confidence = preds[class_idx]
        
        print(f"📸 {filename}: {label} (confidence: {confidence:.3f})")
        results.append(("Fire", label, confidence))
    
    # Test no fire images
    print("\n🌲 Testing NO FIRE images:")
    for filename in nofire_files:
        img_path = os.path.join(nofire_path, filename)
        img = Image.open(img_path).convert("RGB")
        img_resized = img.resize((224, 224))
        
        img_array = image.img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        preds = model.predict(img_array, verbose=0)[0]
        class_idx = np.argmax(preds)
        classes = ["Fire", "No Fire"]
        label = classes[class_idx]
        confidence = preds[class_idx]
        
        print(f"📸 {filename}: {label} (confidence: {confidence:.3f})")
        results.append(("No Fire", label, confidence))
    
    # Calculate accuracy
    correct = sum(1 for true_label, pred_label, _ in results if true_label == pred_label)
    total = len(results)
    accuracy = correct / total if total > 0 else 0
    
    print(f"\n📊 Quick Test Results:")
    print(f"Correct predictions: {correct}/{total}")
    print(f"Accuracy: {accuracy:.2f} ({accuracy*100:.1f}%)")
    
    return results

if __name__ == "__main__":
    # Train the model
    model, history = train_quick_model()
    
    # Test the model
    test_results = test_trained_model(model)
    
    print("\n✅ Quick training complete!")
    print("Now you can use the trained model in your test-model.py")
    print("Model saved in: models/trained/")
    print("Latest version: models/trained/trained_fire_detection_model.h5")
