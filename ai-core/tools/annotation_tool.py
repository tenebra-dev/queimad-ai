"""
Ferramenta de anotação para datasets
Permite anotar bounding boxes em imagens
"""

import cv2
import json
import os
from pathlib import Path

class FireAnnotationTool:
    def __init__(self, images_dir, annotations_file):
        self.images_dir = Path(images_dir)
        self.annotations_file = annotations_file
        self.annotations = self.load_annotations()
        self.current_image = None
        self.current_boxes = []
        self.drawing = False
        self.start_point = None
        
    def load_annotations(self):
        if os.path.exists(self.annotations_file):
            with open(self.annotations_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_annotations(self):
        with open(self.annotations_file, 'w') as f:
            json.dump(self.annotations, f, indent=2)
        print(f"💾 Annotations saved to {self.annotations_file}")
    
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)
        
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            if self.start_point:
                # Add bounding box
                box = {
                    "x": min(self.start_point[0], x),
                    "y": min(self.start_point[1], y),
                    "width": abs(x - self.start_point[0]),
                    "height": abs(y - self.start_point[1]),
                    "class": "fire",
                    "confidence": 1.0
                }
                self.current_boxes.append(box)
                print(f"📦 Added bounding box: {box}")
    
    def annotate_images(self):
        """Main annotation loop"""
        image_files = list(self.images_dir.glob("*.jpg")) + list(self.images_dir.glob("*.png"))
        
        for i, img_path in enumerate(image_files):
            print(f"\n📸 Annotating {img_path.name} ({i+1}/{len(image_files)})")
            
            # Load image
            image = cv2.imread(str(img_path))
            if image is None:
                continue
                
            self.current_image = img_path.name
            self.current_boxes = self.annotations.get(self.current_image, [])
            
            # Create window and set mouse callback
            cv2.namedWindow('Fire Annotation Tool', cv2.WINDOW_NORMAL)
            cv2.setMouseCallback('Fire Annotation Tool', self.mouse_callback)
            
            while True:
                # Draw image with existing boxes
                display_image = image.copy()
                for box in self.current_boxes:
                    cv2.rectangle(display_image, 
                                (box["x"], box["y"]), 
                                (box["x"] + box["width"], box["y"] + box["height"]), 
                                (0, 0, 255), 2)
                    cv2.putText(display_image, box["class"], 
                              (box["x"], box["y"] - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                # Instructions
                cv2.putText(display_image, "Draw boxes around fire. Keys: 's'=save, 'u'=undo, 'n'=next, 'q'=quit", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.imshow('Fire Annotation Tool', display_image)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):  # Save
                    self.annotations[self.current_image] = self.current_boxes
                    self.save_annotations()
                elif key == ord('u'):  # Undo
                    if self.current_boxes:
                        self.current_boxes.pop()
                        print("↩️  Undid last box")
                elif key == ord('n'):  # Next
                    self.annotations[self.current_image] = self.current_boxes
                    break
                elif key == ord('q'):  # Quit
                    self.annotations[self.current_image] = self.current_boxes
                    self.save_annotations()
                    cv2.destroyAllWindows()
                    return
            
            cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python annotation_tool.py <images_directory>")
        sys.exit(1)
    
    images_dir = sys.argv[1]
    annotations_file = "annotations.json"
    
    tool = FireAnnotationTool(images_dir, annotations_file)
    tool.annotate_images()
