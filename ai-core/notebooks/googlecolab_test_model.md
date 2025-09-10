# Load best model
best_model = YOLO('runs/detect/fire_detection_colab/weights/best.pt')

# Test on sample images from dataset
import os
import matplotlib.pyplot as plt
import cv2

test_images_dir = 'wildfire_dataset/test/images'
test_images = [f for f in os.listdir(test_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Test on first 6 images
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, img_name in enumerate(test_images[:6]):
    img_path = os.path.join(test_images_dir, img_name)
    
    # Run detection
    results = best_model(img_path)
    
    # Get annotated image
    annotated = results[0].plot()
    
    # Convert BGR to RGB for matplotlib
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    
    # Display
    axes[i].imshow(annotated_rgb)
    axes[i].set_title(f"Test: {img_name}")
    axes[i].axis('off')
    
    # Print detections
    detections = results[0].boxes
    if detections is not None:
        print(f"\n🔍 {img_name}: {len(detections)} detections")
        for box in detections:
            class_id = int(box.cls[0])
            confidence = box.conf[0]
            class_name = best_model.names[class_id]
            print(f"  - {class_name}: {confidence:.3f}")
    else:
        print(f"\n🔍 {img_name}: No detections")

plt.tight_layout()
plt.show()

print("\n🎉 Visual test completed!")