import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import requests
from io import BytesIO
from PIL import Image
import kagglehub
import os
import random
from datetime import datetime
from PIL import Image
import kagglehub
import os
import random

# Load the locally trained model
print("🔥 Fire Detection with Trained MobileNetV2")
print("=" * 50)

def create_report_folder(test_type):
    """Create a timestamped folder for test reports"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = test_type.lower().replace(" ", "_").replace("-", "_")
    
    # Create main reports directory
    reports_dir = "test_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"📁 Created reports directory: {reports_dir}")
    
    # Create specific test folder
    folder_name = f"{timestamp}_{test_name}"
    test_folder = os.path.join(reports_dir, folder_name)
    os.makedirs(test_folder, exist_ok=True)
    
    print(f"📁 Created test report folder: {test_folder}")
    
    # Create subfolders for organization
    subfolders = [
        "charts",           # Dashboard and analytical charts
        "images",           # Sample images (false positives, true negatives)
        "data",             # Raw data exports (CSV, JSON)
        "summary"           # Text summaries and logs
    ]
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(test_folder, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)
    
    print(f"📂 Created subfolders: {', '.join(subfolders)}")
    return test_folder

def save_test_summary(test_folder, results, test_type, stats):
    """Save a comprehensive text summary of the test"""
    summary_file = os.path.join(test_folder, "summary", f"{test_type.lower().replace(' ', '_')}_summary.txt")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"🔥 FIRE DETECTION MODEL TEST REPORT\n")
        f.write(f"=" * 60 + "\n")
        f.write(f"Test Type: {test_type}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: MobileNetV2 Transfer Learning\n")
        f.write(f"Total Images Tested: {len(results)}\n\n")
        
        f.write(f"📊 PERFORMANCE METRICS\n")
        f.write(f"-" * 30 + "\n")
        for key, value in stats.items():
            if isinstance(value, float):
                f.write(f"{key}: {value:.3f} ({value*100:.1f}%)\n")
            else:
                f.write(f"{key}: {value}\n")
        
        f.write(f"\n🚨 DETAILED RESULTS\n")
        f.write(f"-" * 30 + "\n")
        
        # Organize results by category
        false_positives = []
        false_negatives = []
        true_positives = []
        true_negatives = []
        
        for result in results:
            if len(result) >= 6:
                filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob = result
                is_actually_fire = filename.startswith('fire_')
                
                if predicted_fire and is_actually_fire:
                    true_positives.append((filename, confidence))
                elif predicted_fire and not is_actually_fire:
                    false_positives.append((filename, confidence))
                elif not predicted_fire and not is_actually_fire:
                    true_negatives.append((filename, confidence))
                else:
                    false_negatives.append((filename, confidence))
        
        # Write categorized results
        categories = [
            ("TRUE POSITIVES (Fire Correctly Detected)", true_positives),
            ("TRUE NEGATIVES (No Fire Correctly Detected)", true_negatives),
            ("FALSE POSITIVES (Incorrectly Detected as Fire)", false_positives),
            ("FALSE NEGATIVES (Missed Fire Detection)", false_negatives)
        ]
        
        for category_name, category_list in categories:
            f.write(f"\n{category_name}:\n")
            if category_list:
                # Sort by confidence
                category_list.sort(key=lambda x: x[1], reverse=True)
                for i, (filename, conf) in enumerate(category_list, 1):
                    f.write(f"  {i:3d}. {filename:<25} | Confidence: {conf:.3f}\n")
            else:
                f.write("  None\n")
    
    print(f"📄 Test summary saved: {summary_file}")
    return summary_file

def save_data_exports(report_folder, results, test_type):
    """Save test results in CSV and JSON formats for further analysis"""
    import json
    
    # Prepare data for export
    export_data = []
    for result in results:
        if len(result) >= 6:
            filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob = result
            is_actually_fire = filename.startswith('fire_')
            
            export_data.append({
                'filename': str(filename),
                'actual_label': 'fire' if is_actually_fire else 'nofire',
                'predicted_label': 'fire' if predicted_fire else 'nofire',
                'predicted_fire': bool(predicted_fire),
                'is_correct': bool(is_correct),
                'confidence': float(confidence),
                'fire_probability': float(fire_prob),
                'nofire_probability': float(nofire_prob),
                'prediction_type': get_prediction_type(is_actually_fire, predicted_fire)
            })
    
    # Save as JSON
    json_file = os.path.join(report_folder, "data", f"{test_type.lower().replace(' ', '_')}_results.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'test_type': test_type,
            'timestamp': datetime.now().isoformat(),
            'total_images': len(export_data),
            'results': export_data
        }, f, indent=2, ensure_ascii=False)
    
    # Save as CSV
    csv_file = os.path.join(report_folder, "data", f"{test_type.lower().replace(' ', '_')}_results.csv")
    with open(csv_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("filename,actual_label,predicted_label,is_correct,confidence,fire_probability,nofire_probability,prediction_type\n")
        
        # Data rows
        for item in export_data:
            f.write(f"{item['filename']},{item['actual_label']},{item['predicted_label']},{item['is_correct']},{item['confidence']:.6f},{item['fire_probability']:.6f},{item['nofire_probability']:.6f},{item['prediction_type']}\n")
    
    print(f"📊 Data exported to: {json_file}")
    print(f"📊 Data exported to: {csv_file}")
    
    return json_file, csv_file

def get_prediction_type(is_actually_fire, predicted_fire):
    """Determine the type of prediction (TP, TN, FP, FN)"""
    if is_actually_fire and predicted_fire:
        return "True Positive"
    elif not is_actually_fire and not predicted_fire:
        return "True Negative"
    elif not is_actually_fire and predicted_fire:
        return "False Positive"
    else:  # is_actually_fire and not predicted_fire
        return "False Negative"

# Check for local trained model first
local_model_path = "models/trained/trained_fire_detection_model.h5"

if os.path.exists(local_model_path):
    print(f"✅ Found local trained model: {local_model_path}")
    print("Loading trained fire detection model...")
    model = tf.keras.models.load_model(local_model_path)
    print("✅ Trained model loaded successfully!")
    print(f"Model input shape: {model.input_shape}")
    print(f"Model output shape: {model.output_shape}")
else:
    print("❌ Trained model not found!")
    print(f"Please run 'poetry run python quick_train.py' first to train a model.")
    print(f"Looking for: {local_model_path}")
    exit(1)

# Download dataset for testing  
print("\nDownloading test dataset...")
dataset_path = kagglehub.dataset_download("alik05/forest-fire-dataset")
base_path = os.path.join(dataset_path, "Forest Fire Dataset")
train_fire_path = os.path.join(base_path, "Training", "fire")
train_nofire_path = os.path.join(base_path, "Training", "nofire")
test_path = os.path.join(base_path, "Testing")

print(f"Dataset available at: {dataset_path}")
print(f"Training - Fire images: {len(os.listdir(train_fire_path)) if os.path.exists(train_fire_path) else 0}")
print(f"Training - No Fire images: {len(os.listdir(train_nofire_path)) if os.path.exists(train_nofire_path) else 0}")
print(f"Testing images: {len(os.listdir(test_path)) if os.path.exists(test_path) else 0}")

# Check test images structure
if os.path.exists(test_path):
    test_files = [f for f in os.listdir(test_path) if f.endswith('.jpg')]
    print(f"Total test images available: {len(test_files)}")
    
    # Check naming pattern to understand labels
    fire_test_files = [f for f in test_files if 'fire' in f.lower()]
    print(f"Test images with 'fire' in name: {len(fire_test_files)}")
    print(f"Sample test files: {test_files[:5]}")
else:
    print("❌ Test path not found!")

# Function to preprocess image and make prediction (based on Kaggle example)
def predict_fire_from_url(img_url):
    """
    Predict fire from image URL using the pre-trained model
    Based on: https://www.kaggle.com/code/datascientist97/example-code-to-use
    """
    try:
        # Download image with headers (to avoid blocking)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(img_url, headers=headers, stream=True)
        response.raise_for_status()

        if "image" not in response.headers.get("Content-Type", ""):
            raise ValueError(f"URL does not contain an image: {img_url}")

        # Open and resize image
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img_resized = img.resize((224, 224))  # MobileNetV2 input size

        # Convert to array and normalize (same as original code)
        img_array = image.img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        # Make prediction
        preds = model.predict(img_array, verbose=0)[0]
        class_idx = np.argmax(preds)
        classes = ["Fire", "No Fire"]  # Adjust based on your model's classes
        label = classes[class_idx]
        confidence = preds[class_idx]
        
        # Display result
        plt.figure(figsize=(10, 6))
        plt.imshow(img_resized)
        plt.axis("off")
        plt.title(f"Prediction: {label} (Confidence: {confidence:.3f})")
        plt.show()
        
        print(f"🌐 URL: {img_url}")
        print(f"🔥 Prediction: {label}")
        print(f"📊 Confidence: {confidence:.3f}")
        print(f"📈 Raw scores - Fire: {preds[0]:.3f}, No Fire: {preds[1]:.3f}")
        print("-" * 60)
        
        return label, confidence
        
    except Exception as e:
        print(f"❌ Error processing {img_url}: {e}")
        return None, None

def predict_fire_from_file(img_path):
    """
    Predict fire from local image file
    """
    try:
        # Load and preprocess image
        img = Image.open(img_path).convert("RGB")
        img_resized = img.resize((224, 224))
        
        # Convert to array and normalize
        img_array = image.img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        preds = model.predict(img_array, verbose=0)[0]
        class_idx = np.argmax(preds)
        classes = ["Fire", "No Fire"]
        label = classes[class_idx]
        confidence = preds[class_idx]
        
        # Display result
        plt.figure(figsize=(10, 6))
        plt.imshow(img_resized)
        plt.axis("off")
        plt.title(f"Prediction: {label} (Confidence: {confidence:.3f})")
        plt.show()
        
        print(f"📸 File: {os.path.basename(img_path)}")
        print(f"🔥 Prediction: {label}")
        print(f"📊 Confidence: {confidence:.3f}")
        print(f"📈 Raw scores - Fire: {preds[0]:.3f}, No Fire: {preds[1]:.3f}")
        print("-" * 60)
        
        return label, confidence
        
    except Exception as e:
        print(f"❌ Error processing {img_path}: {e}")
        return None, None

def visualize_predictions(results, test_type="Test", report_folder=None):
    """Create a visual summary of model predictions"""
    if not results:
        print("❌ No results to visualize!")
        return
    
    # Create report folder if not provided
    if report_folder is None:
        report_folder = create_report_folder(test_type)
    
    # Organize results by prediction type
    fire_predictions = []
    nofire_predictions = []
    false_positives = []
    false_negatives = []
    
    for result in results:
        if len(result) >= 6:  # Full result with ground truth
            filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob = result
            
            # Determine ground truth from filename
            is_actually_fire = filename.startswith('fire_')
            
            if predicted_fire and is_actually_fire:
                fire_predictions.append((filename, confidence, "✅ True Positive"))
            elif predicted_fire and not is_actually_fire:
                false_positives.append((filename, confidence, "❌ False Positive"))
            elif not predicted_fire and not is_actually_fire:
                nofire_predictions.append((filename, confidence, "✅ True Negative"))
            else:  # not predicted_fire and is_actually_fire
                false_negatives.append((filename, confidence, "❌ False Negative"))
    
    print(f"\n🎨 VISUAL PREDICTION SUMMARY - {test_type}")
    print("=" * 70)
    
    # Summary stats
    total = len(results)
    correct = len(fire_predictions) + len(nofire_predictions)
    accuracy = correct / total * 100 if total > 0 else 0
    
    print(f"📊 Overall Statistics:")
    print(f"   Total images: {total}")
    print(f"   Correct predictions: {correct}")
    print(f"   Accuracy: {accuracy:.1f}%")
    print(f"   False Positives: {len(false_positives)}")
    print(f"   False Negatives: {len(false_negatives)}")
    
    # Save comprehensive statistics
    stats = {
        "Total Images": total,
        "Correct Predictions": correct,
        "Accuracy": accuracy / 100,
        "True Positives": len(fire_predictions),
        "True Negatives": len(nofire_predictions),
        "False Positives": len(false_positives),
        "False Negatives": len(false_negatives),
        "False Positive Rate": len(false_positives) / total if total > 0 else 0,
        "False Negative Rate": len(false_negatives) / total if total > 0 else 0
    }
    
    # Save text summary
    save_test_summary(report_folder, results, test_type, stats)
    
    # Save data exports
    save_data_exports(report_folder, results, test_type)
    
    # Show samples from each category
    categories = [
        ("🔥 FIRE DETECTED (Correct)", fire_predictions, "green"),
        ("🌲 NO FIRE DETECTED (Correct)", nofire_predictions, "blue"),
        ("🚨 FALSE POSITIVES (Wrong - Detected as Fire)", false_positives, "red"),
        ("⚠️ FALSE NEGATIVES (Wrong - Missed Fire)", false_negatives, "orange")
    ]
    
    for category_name, category_results, color in categories:
        if not category_results:
            continue
            
        print(f"\n{category_name}")
        print("-" * 60)
        print(f"Count: {len(category_results)} images")
        
        # Show top 5 by confidence
        sorted_results = sorted(category_results, key=lambda x: x[1], reverse=True)
        top_results = sorted_results[:5]
        
        print(f"Top samples by confidence:")
        for i, (filename, conf, status) in enumerate(top_results, 1):
            print(f"  {i}. {filename:<20} | Confidence: {conf:.3f} | {status}")
        
        if len(category_results) > 5:
            print(f"  ... and {len(category_results) - 5} more images")
    
    # Create matplotlib visualization
    if len(results) > 0:
        create_prediction_plots(fire_predictions, nofire_predictions, false_positives, false_negatives, test_type, report_folder)
        
        # Ask if user wants to see sample images
        try:
            if false_positives or false_negatives:
                show_images = input("\n🖼️  Do you want to see sample images of predictions? (y/n): ").strip().lower()
                if show_images in ['y', 'yes', '1', 'true']:
                    print("📸 Creating image galleries...")
                    show_sample_images(results, test_type, show_false_positives=len(false_positives) > 0, report_folder=report_folder)
        except KeyboardInterrupt:
            print("\n👋 Skipping image display...")
        except Exception:
            print("📋 Continuing without image display...")
    
    print(f"\n📁 All reports saved in: {report_folder}")
    return report_folder

def show_sample_images(results, test_type="Test", show_false_positives=True, report_folder=None):
    """Show sample images from the test results"""
    
    if not results:
        return
    
    # Get false positives and true negatives
    false_positives = []
    true_negatives = []
    
    for result in results:
        if len(result) >= 6:
            filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob = result
            is_actually_fire = filename.startswith('fire_')
            
            if predicted_fire and not is_actually_fire:  # False positive
                false_positives.append((filename, confidence))
            elif not predicted_fire and not is_actually_fire:  # True negative
                true_negatives.append((filename, confidence))
    
    if show_false_positives and false_positives:
        # Show top 6 false positives
        false_positives.sort(key=lambda x: x[1], reverse=True)
        show_images_grid(false_positives[:6], "🚨 FALSE POSITIVES - Most Confident Mistakes", "red", report_folder)
    
    # Show some high-confidence true negatives for comparison
    true_negatives.sort(key=lambda x: x[1], reverse=True)
    show_images_grid(true_negatives[:6], "✅ TRUE NEGATIVES - High Confidence Correct", "green", report_folder)

def show_images_grid(image_list, title, color, report_folder=None):
    """Display a grid of images with their info"""
    
    if not image_list:
        return
    
    try:
        # Create subplot grid
        n_images = min(len(image_list), 6)
        cols = 3
        rows = (n_images + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
        fig.suptitle(title, fontsize=16, color=color, fontweight='bold')
        
        # Ensure axes is always a list
        if rows == 1:
            axes = [axes] if cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, (filename, confidence) in enumerate(image_list[:n_images]):
            img_path = os.path.join(test_path, filename)
            
            try:
                # Load and display image
                img = Image.open(img_path)
                axes[i].imshow(img)
                axes[i].set_title(f"{filename}\nConfidence: {confidence:.3f}", 
                                fontsize=10, color=color)
                axes[i].axis('off')
            except Exception as e:
                axes[i].text(0.5, 0.5, f"Error loading\n{filename}", 
                           ha='center', va='center', transform=axes[i].transAxes)
                axes[i].axis('off')
        
        # Hide empty subplots
        for i in range(n_images, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        
        # Save the grid to the appropriate folder
        if report_folder:
            grid_filename = f"{title.lower().replace(' ', '_').replace('🚨', '').replace('✅', '').strip()}.png"
            grid_path = os.path.join(report_folder, "images", grid_filename)
        else:
            grid_filename = f"{title.lower().replace(' ', '_').replace('🚨', '').replace('✅', '').strip()}.png"
            grid_path = grid_filename
            
        plt.savefig(grid_path, dpi=150, bbox_inches='tight')
        print(f"📸 Image grid saved as: {grid_path}")
        
        # Try to show
        try:
            plt.show(block=False)
        except:
            pass
        
        # Try to open with default viewer
        try:
            import subprocess
            subprocess.run(["start", grid_path], shell=True, check=False)
        except:
            pass
            
        plt.close()
        
    except Exception as e:
        print(f"❌ Error creating image grid: {e}")

def create_prediction_plots(fire_preds, nofire_preds, false_pos, false_neg, test_type, report_folder=None):
    """Create matplotlib plots showing prediction distribution"""
    
    # Confidence distribution plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Model Predictions Analysis - {test_type}', fontsize=16, fontweight='bold')
    
    # Plot 1: Confidence distribution for correct predictions
    if fire_preds or nofire_preds:
        fire_confs = [conf for _, conf, _ in fire_preds]
        nofire_confs = [conf for _, conf, _ in nofire_preds]
        
        ax1.hist(fire_confs, bins=20, alpha=0.7, label=f'Fire Detected ({len(fire_confs)})', color='red')
        ax1.hist(nofire_confs, bins=20, alpha=0.7, label=f'No Fire Detected ({len(nofire_confs)})', color='blue')
        ax1.set_title('Confidence Distribution - Correct Predictions')
        ax1.set_xlabel('Confidence Score')
        ax1.set_ylabel('Count')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    
    # Plot 2: False positives analysis
    if false_pos:
        fp_confs = [conf for _, conf, _ in false_pos]
        ax2.hist(fp_confs, bins=10, alpha=0.7, color='orange', edgecolor='red')
        ax2.set_title(f'False Positives Confidence ({len(false_pos)} images)')
        ax2.set_xlabel('Confidence Score')
        ax2.set_ylabel('Count')
        ax2.axvline(x=0.5, color='red', linestyle='--', label='Decision Threshold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No False Positives!', transform=ax2.transAxes, 
                ha='center', va='center', fontsize=14, color='green', weight='bold')
        ax2.set_title('False Positives Analysis')
    
    # Plot 3: Performance metrics pie chart
    correct_count = len(fire_preds) + len(nofire_preds)
    fp_count = len(false_pos)
    fn_count = len(false_neg)
    
    labels = []
    sizes = []
    colors = []
    
    if correct_count > 0:
        labels.append(f'Correct\n({correct_count})')
        sizes.append(correct_count)
        colors.append('lightgreen')
    
    if fp_count > 0:
        labels.append(f'False Pos\n({fp_count})')
        sizes.append(fp_count)
        colors.append('lightcoral')
    
    if fn_count > 0:
        labels.append(f'False Neg\n({fn_count})')
        sizes.append(fn_count)
        colors.append('orange')
    
    if labels:
        ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Prediction Results Distribution')
    
    # Plot 4: Summary statistics
    ax4.axis('off')
    total = correct_count + fp_count + fn_count
    accuracy = correct_count / total * 100 if total > 0 else 0
    precision = len(fire_preds) / (len(fire_preds) + fp_count) * 100 if (len(fire_preds) + fp_count) > 0 else 0
    recall = len(fire_preds) / (len(fire_preds) + fn_count) * 100 if (len(fire_preds) + fn_count) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate rates with zero-division protection
    fp_rate = fp_count / total * 100 if total > 0 else 0
    fn_rate = fn_count / total * 100 if total > 0 else 0
    
    stats_text = f"""MODEL PERFORMANCE METRICS

Overall Accuracy: {accuracy:.1f}%
Fire Detection (Precision): {precision:.1f}%
Fire Recall: {recall:.1f}%
F1-Score: {f1:.1f}%

Detailed Breakdown:
  True Positives (Fire): {len(fire_preds)}
  True Negatives (No Fire): {len(nofire_preds)}
  False Positives: {fp_count}
  False Negatives: {fn_count}

False Positive Rate: {fp_rate:.1f}%
False Negative Rate: {fn_rate:.1f}%
    """
    
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    
    # Save the plot to the appropriate folder
    if report_folder:
        plot_filename = f'prediction_analysis_{test_type.lower().replace(" ", "_")}.png'
        plot_path = os.path.join(report_folder, "charts", plot_filename)
    else:
        plot_filename = f'prediction_analysis_{test_type.lower().replace(" ", "_")}.png'
        plot_path = plot_filename
        
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Visualization saved as: {plot_path}")
    
    # Try to show the plot
    try:
        plt.show(block=False)
        print(f"🎨 Visual analysis displayed! Check the plot window.")
    except Exception as e:
        print(f"⚠️  Could not display plot automatically: {e}")
        print(f"📁 Please open the file manually: {plot_path}")
    
    # Also try to open the file with the default image viewer
    try:
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            subprocess.run(["start", plot_path], shell=True, check=False)
            print(f"🖼️  Attempting to open with default image viewer...")
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", plot_path], check=False)
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", plot_path], check=False)
    except Exception as e:
        print(f"📁 Please open the file manually: {plot_path}")
    
    plt.close()  # Close the figure to free memory
    
    return plot_path

def test_only_nofire_images():
    """Test specifically with NO FIRE images to analyze false positive rate"""
    print("\n🧪 NO-FIRE SPECIFIC TEST - Analyzing false positive rate...")
    
    if not os.path.exists(test_path):
        print("❌ Test dataset not found!")
        return []
    
    # Get only nofire files
    test_files = [f for f in os.listdir(test_path) if f.endswith('.jpg')]
    nofire_files = [f for f in test_files if f.startswith('nofire_')]
    
    if len(nofire_files) == 0:
        print("❌ No nofire images found in test dataset!")
        return []
    
    print(f"Found {len(nofire_files)} NO-FIRE images")
    print(f"Sample files: {nofire_files[:5]}")
    
    results = []
    correct = 0
    false_positives = 0
    confidence_scores = []
    false_positive_details = []
    
    print(f"\n🌲 Testing {len(nofire_files)} NO-FIRE images...")
    print("Looking for false positives (incorrectly detected as fire)...")
    
    for i, filename in enumerate(nofire_files):
        img_path = os.path.join(test_path, filename)
        
        try:
            # Load and preprocess image
            img = Image.open(img_path).convert("RGB")
            img_resized = img.resize((224, 224))
            
            img_array = image.img_to_array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Make prediction
            preds = model.predict(img_array, verbose=0)[0]
            fire_prob = preds[0]
            nofire_prob = preds[1]
            
            # Determine prediction (fire if fire_prob > 0.5)
            predicted_fire = fire_prob > 0.5
            is_correct = not predicted_fire  # Should be False for nofire images
            confidence = max(fire_prob, nofire_prob)
            
            # Store results
            results.append((filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob))
            confidence_scores.append(confidence)
            
            if is_correct:
                correct += 1
            else:
                false_positives += 1
                false_positive_details.append({
                    'filename': filename,
                    'fire_prob': fire_prob,
                    'confidence': confidence
                })
            
            # Progress update every 25 images
            if (i + 1) % 25 == 0 or (i + 1) == len(nofire_files):
                current_accuracy = correct / (i + 1) * 100
                current_fp_rate = false_positives / (i + 1) * 100
                print(f"Progress: {i + 1}/{len(nofire_files)} - Accuracy: {current_accuracy:.1f}% - False Positive Rate: {current_fp_rate:.1f}%")
        
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    # Calculate final metrics
    total = len(results)
    accuracy = correct / total if total > 0 else 0
    fp_rate = false_positives / total if total > 0 else 0
    avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
    
    print("\n" + "="*60)
    print("📊 NO-FIRE IMAGES TEST RESULTS")
    print("="*60)
    
    print(f"🌲 Total NO-FIRE images tested: {total}")
    print(f"✅ Correctly identified as NO-FIRE: {correct}")
    print(f"❌ Incorrectly identified as FIRE: {false_positives}")
    print(f"📊 Accuracy (Correct NO-FIRE detection): {accuracy:.3f} ({accuracy*100:.1f}%)")
    print(f"🚨 False Positive Rate: {fp_rate:.3f} ({fp_rate*100:.1f}%)")
    print(f"📈 Average Confidence: {avg_confidence:.3f}")
    
    # Show false positive details
    if false_positive_details:
        print(f"\n🚨 FALSE POSITIVE ANALYSIS:")
        print(f"Images incorrectly detected as FIRE:")
        for i, fp in enumerate(false_positive_details[:10]):  # Show first 10
            print(f"  {i+1}. {fp['filename']} - Fire prob: {fp['fire_prob']:.3f} (conf: {fp['confidence']:.3f})")
        
        if len(false_positive_details) > 10:
            print(f"  ... and {len(false_positive_details) - 10} more")
        
        # Confidence distribution of false positives
        fp_confidences = [fp['fire_prob'] for fp in false_positive_details]
        high_conf_fps = [fp for fp in fp_confidences if fp > 0.8]
        medium_conf_fps = [fp for fp in fp_confidences if 0.5 < fp <= 0.8]
        
        print(f"\n📊 False Positive Confidence Distribution:")
        print(f"  High confidence (>0.8): {len(high_conf_fps)} images")
        print(f"  Medium confidence (0.5-0.8): {len(medium_conf_fps)} images")
    
    # Quality assessment
    print(f"\n🎖️ NO-FIRE Detection Quality Assessment:")
    if fp_rate < 0.05:  # Less than 5% false positives
        print("   🌟 EXCELLENT - Very low false positive rate!")
    elif fp_rate < 0.10:  # Less than 10% false positives
        print("   ✅ GOOD - Acceptable false positive rate")
    elif fp_rate < 0.20:  # Less than 20% false positives
        print("   ⚠️  FAIR - Consider model improvement")
    else:
        print("   ❌ NEEDS IMPROVEMENT - High false positive rate")
    
    # Create visual summary
    print(f"\n🎨 Generating visual analysis...")
    report_folder = visualize_predictions(results, "NO-FIRE Specific Test")
    
    return results

def test_with_full_test_dataset():
    """Test the model with all 380 test images from the dataset"""
    
    print(f"\n🧪 COMPREHENSIVE TEST - Using all test images...")
    
    try:
        if not os.path.exists(test_path):
            print("❌ Test path not found!")
            return []
            
        # Get all test images
        test_files = [f for f in os.listdir(test_path) if f.endswith('.jpg')]
        print(f"Found {len(test_files)} test images")
        
        # Analyze filename patterns to determine ground truth
        # Correct pattern: fire_xxxx.jpg vs nofire_xxxx.jpg
        fire_test_files = [f for f in test_files if f.startswith('fire_')]
        nofire_test_files = [f for f in test_files if f.startswith('nofire_')]
        
        print(f"Fire test images: {len(fire_test_files)}")
        print(f"No-fire test images: {len(nofire_test_files)}")
        
        # Verify we have the expected 50/50 split
        if len(fire_test_files) + len(nofire_test_files) != len(test_files):
            print("⚠️  Warning: Some files don't match expected pattern!")
            unmatched = [f for f in test_files if not (f.startswith('fire_') or f.startswith('nofire_'))]
            print(f"Unmatched files: {unmatched[:5]}")
        
        # Show sample filenames for verification
        print(f"Sample fire files: {fire_test_files[:3]}")
        print(f"Sample no-fire files: {nofire_test_files[:3]}")
        
        results = []
        correct_fire = 0
        correct_nofire = 0
        total_fire = len(fire_test_files)
        total_nofire = len(nofire_test_files)
        
        # Test fire images
        print(f"\n🔥 Testing {total_fire} FIRE images...")
        for i, filename in enumerate(fire_test_files):
            img_path = os.path.join(test_path, filename)
            
            # Load and preprocess image
            img = Image.open(img_path).convert("RGB")
            img_resized = img.resize((224, 224))
            img_array = image.img_to_array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Make prediction
            preds = model.predict(img_array, verbose=0)[0]
            fire_prob = preds[0]
            nofire_prob = preds[1]
            predicted_fire = fire_prob > 0.5  # True if fire predicted
            confidence = max(fire_prob, nofire_prob)
            
            # Check if correct
            is_correct = predicted_fire  # Should be True for fire images
            if is_correct:
                correct_fire += 1
                
            # Store results in format expected by visualize_predictions
            results.append((filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob))
            
            # Progress update
            if (i + 1) % 25 == 0 or (i + 1) == total_fire:
                print(f"Progress: {i + 1}/{total_fire} - Current accuracy: {correct_fire/(i+1)*100:.1f}%")
        
        # Test no-fire images
        print(f"\n🌲 Testing {total_nofire} NO-FIRE images...")
        for i, filename in enumerate(nofire_test_files):
            img_path = os.path.join(test_path, filename)
            
            # Load and preprocess image
            img = Image.open(img_path).convert("RGB")
            img_resized = img.resize((224, 224))
            img_array = image.img_to_array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Make prediction
            preds = model.predict(img_array, verbose=0)[0]
            fire_prob = preds[0]
            nofire_prob = preds[1]
            predicted_fire = fire_prob > 0.5  # True if fire predicted
            confidence = max(fire_prob, nofire_prob)
            
            # Check if correct
            is_correct = not predicted_fire  # Should be False for no-fire images
            if is_correct:
                correct_nofire += 1
                
            # Store results in format expected by visualize_predictions
            results.append((filename, predicted_fire, confidence, is_correct, fire_prob, nofire_prob))
            
            # Progress update
            if (i + 1) % 25 == 0 or (i + 1) == total_nofire:
                print(f"Progress: {i + 1}/{total_nofire} - Current accuracy: {correct_nofire/(i+1)*100:.1f}%")
        
        # Calculate comprehensive metrics
        total_correct = correct_fire + correct_nofire
        total_images = total_fire + total_nofire
        overall_accuracy = total_correct / total_images if total_images > 0 else 0
        
        fire_accuracy = correct_fire / total_fire if total_fire > 0 else 0
        nofire_accuracy = correct_nofire / total_nofire if total_nofire > 0 else 0
        
        # Calculate confidence statistics
        confidences = [conf for _, _, conf, _, _, _ in results]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        correct_confidences = [conf for _, _, conf, correct, _, _ in results if correct]
        incorrect_confidences = [conf for _, _, conf, correct, _, _ in results if not correct]
        
        avg_correct_confidence = sum(correct_confidences) / len(correct_confidences) if correct_confidences else 0
        avg_incorrect_confidence = sum(incorrect_confidences) / len(incorrect_confidences) if incorrect_confidences else 0
        
        print(f"\n" + "="*60)
        print(f"📊 COMPREHENSIVE TEST RESULTS")
        print(f"="*60)
        print(f"🔥 Fire Detection:")
        print(f"   Correct: {correct_fire}/{total_fire}")
        print(f"   Accuracy: {fire_accuracy:.3f} ({fire_accuracy*100:.1f}%)")
        
        print(f"\n🌲 No-Fire Detection:")
        print(f"   Correct: {correct_nofire}/{total_nofire}")
        print(f"   Accuracy: {nofire_accuracy:.3f} ({nofire_accuracy*100:.1f}%)")
        
        print(f"\n🎯 Overall Performance:")
        print(f"   Total Correct: {total_correct}/{total_images}")
        print(f"   Overall Accuracy: {overall_accuracy:.3f} ({overall_accuracy*100:.1f}%)")
        
        print(f"\n📈 Confidence Analysis:")
        print(f"   Average Confidence: {avg_confidence:.3f}")
        print(f"   Avg Confidence (Correct): {avg_correct_confidence:.3f}")
        print(f"   Avg Confidence (Incorrect): {avg_incorrect_confidence:.3f}")
        
        # Classification metrics
        true_positives = correct_fire
        false_positives = total_nofire - correct_nofire
        false_negatives = total_fire - correct_fire
        true_negatives = correct_nofire
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\n🔬 Advanced Metrics:")
        print(f"   Precision: {precision:.3f} ({precision*100:.1f}%)")
        print(f"   Recall: {recall:.3f} ({recall*100:.1f}%)")
        print(f"   F1-Score: {f1_score:.3f}")
        
        print(f"\n🎖️ Model Quality Assessment:")
        if overall_accuracy >= 0.9:
            print("   🌟 EXCELLENT - Ready for production!")
        elif overall_accuracy >= 0.8:
            print("   ✅ GOOD - Suitable for most applications")
        elif overall_accuracy >= 0.7:
            print("   ⚠️  FAIR - Consider more training")
        else:
            print("   ❌ POOR - Needs significant improvement")
        
        # Create visual summary
        print(f"\n🎨 Generating comprehensive visual analysis...")
        report_folder = visualize_predictions(results, "Comprehensive Test")
            
        return results
        
    except Exception as e:
        print(f"❌ Error in comprehensive testing: {e}")
        return []

def test_with_dataset_images(num_samples=3):
    """Test the model with random images from the training dataset (quick test)"""
    
    print(f"\n🧪 QUICK TEST - Using {num_samples} random images from training set...")
    
    try:
        # Get random images
        fire_files = [f for f in os.listdir(train_fire_path) if f.endswith('.jpg')][:num_samples]
        nofire_files = [f for f in os.listdir(train_nofire_path) if f.endswith('.jpg')][:num_samples]
        
        results = []
        
        # Test fire images
        print("\n🔥 Testing FIRE images:")
        for filename in fire_files:
            img_path = os.path.join(train_fire_path, filename)
            label, confidence = predict_fire_from_file(img_path)
            if label:
                results.append(("Fire", label, confidence))
        
        # Test no fire images  
        print("\n🌲 Testing NO FIRE images:")
        for filename in nofire_files:
            img_path = os.path.join(train_nofire_path, filename)
            label, confidence = predict_fire_from_file(img_path)
            if label:
                results.append(("No Fire", label, confidence))
        
        # Calculate accuracy
        correct = sum(1 for true_label, pred_label, _ in results if true_label == pred_label)
        total = len(results)
        accuracy = correct / total if total > 0 else 0
        
        print(f"\n📊 Quick Test Results:")
        print(f"Correct predictions: {correct}/{total}")
        print(f"Accuracy: {accuracy:.2f} ({accuracy*100:.1f}%)")
        
        return results
        
    except Exception as e:
        print(f"❌ Error testing with dataset: {e}")
        return []

# Main execution
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔥 FIRE DETECTION MODEL TEST")
    print(f"Using locally trained MobileNetV2 model")
    print("="*60)
    
    # Ask user for test type
    print("\nChoose test type:")
    print("1. Quick test (6 images from training set)")
    print("2. Comprehensive test (all 380 test images)")
    print("3. NO-FIRE specific test (analyze false positives)")
    print("4. Both comprehensive and no-fire tests")
    
    # Get user input
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ["1", "2", "3", "4"]:
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            exit(0)
        except Exception:
            print("❌ Invalid input. Please enter a number between 1-4.")
    
    print(f"\n🚀 Starting test option {choice}...")
    
    if choice == "1":
        # Quick test only
        test_results = test_with_dataset_images(3)
        
    elif choice == "2":
        # Comprehensive test only
        print(f"\n⏳ Running comprehensive test with all test images...")
        print("This may take a few minutes...")
        test_results = test_with_full_test_dataset()
        
    elif choice == "3":
        # NO-FIRE specific test
        print(f"\n🔍 Running NO-FIRE specific test...")
        print("Analyzing false positive rate...")
        test_results = test_only_nofire_images()
        
    elif choice == "4":
        # Comprehensive + NO-FIRE tests
        print(f"\n⏳ Running comprehensive test first...")
        print("This may take a few minutes...")
        comprehensive_results = test_with_full_test_dataset()
        
        print(f"\n🔍 Now running NO-FIRE specific test...")
        nofire_results = test_only_nofire_images()
        test_results = comprehensive_results  # For final summary
        
    else:
        # Both tests
        print(f"\n�‍♂️ Running quick test first...")
        quick_results = test_with_dataset_images(3)
        
        print(f"\n⏳ Now running comprehensive test...")
        print("This may take a few minutes...")
        test_results = test_with_full_test_dataset()
    
    # Test with URLs only for quick test
    if choice == "1":
        print("\n🌐 Testing with URL images:")
        
        test_urls = [
            "https://www.chooch.com/wp-content/uploads/2023/05/wildfire-flames-smoke.jpg",
            "https://onetreeplanted.org/cdn/shop/articles/Forest_Fog_1800x.jpg?v=1682535224"
        ]
        
        for url in test_urls:
            predict_fire_from_url(url)
    
    print("\n✅ Fire detection testing complete!")
    print("Your trained model performance has been thoroughly evaluated!")
    
    # Ask if user wants to see detailed analysis
    if test_results and choice in ["2", "3", "4"]:
        try:
            show_details = input("\n🎨 Do you want to see detailed visual analysis? (y/n): ").strip().lower()
            if show_details in ['y', 'yes', '1', 'true']:
                print("\n📊 Opening detailed analysis...")
                # Visualization is already called within the test functions
            else:
                print("📋 Skipping detailed visualization.")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
        except Exception:
            print("📋 Skipping detailed visualization.")
    
    # Final summary for comprehensive test
    if choice in ["2", "4"] and test_results:
        total_tested = len(test_results)
        if len(test_results[0]) >= 4:  # Check if results have is_correct field
            correct = sum(1 for result in test_results if len(result) >= 4 and result[3])
        else:
            correct = 0
        
        print(f"\n🎯 FINAL SUMMARY:")
        print(f"Total images tested: {total_tested}")
        if total_tested > 0:
            print(f"Overall accuracy: {correct/total_tested*100:.1f}%")
            
            if correct/total_tested >= 0.8:
                print("🌟 Your model is performing excellently!")
            else:
                print("⚠️  Consider additional training to improve accuracy.")