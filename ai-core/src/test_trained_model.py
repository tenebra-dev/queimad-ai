"""
🔥 Teste do Modelo YOLOv8 Treinado
Script para testar o modelo baixado do Google Colab
"""

import os
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def load_trained_model(model_path="runs/detect/fire_detection_yolo/weights/best.pt"):
    """Carregar modelo treinado"""
    
    if not os.path.exists(model_path):
        print(f"❌ Modelo não encontrado: {model_path}")
        print("📥 Baixe o modelo do Google Colab primeiro!")
        return None
    
    try:
        model = YOLO(model_path)
        print(f"✅ Modelo carregado: {model_path}")
        print(f"📋 Classes do modelo: {model.names}")
        return model
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return None

def test_single_image(model, image_path, conf_threshold=0.5):
    """Testar em uma única imagem"""
    
    if not os.path.exists(image_path):
        print(f"❌ Imagem não encontrada: {image_path}")
        return None
    
    # Run detection
    results = model(image_path, conf=conf_threshold)
    
    # Get results
    detections = []
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = box.conf[0].item()
                class_id = int(box.cls[0].item())
                class_name = model.names[class_id]
                
                detections.append({
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': [int(x1), int(y1), int(x2), int(y2)]
                })
    
    return detections, results

def visualize_detection(image_path, detections, results):
    """Visualizar detecções"""
    
    # Load original image
    original_img = cv2.imread(image_path)
    original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    
    # Get annotated image from YOLO
    annotated = results[0].plot()
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    
    # Create comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original image
    axes[0].imshow(original_rgb)
    axes[0].set_title('Imagem Original')
    axes[0].axis('off')
    
    # Annotated image
    axes[1].imshow(annotated_rgb)
    axes[1].set_title(f'Detecções Encontradas: {len(detections)}')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Print detection details
    if detections:
        print(f"\n🎯 DETECÇÕES ENCONTRADAS:")
        for i, det in enumerate(detections, 1):
            print(f"{i}. {det['class'].upper()}")
            print(f"   Confiança: {det['confidence']:.3f}")
            print(f"   Posição: {det['bbox']}")
    else:
        print("✅ Nenhuma detecção encontrada")

def test_dataset_folder(model, images_folder, conf_threshold=0.5):
    """Testar em pasta de imagens"""
    
    if not os.path.exists(images_folder):
        print(f"❌ Pasta não encontrada: {images_folder}")
        return
    
    # Get all images
    image_files = [f for f in os.listdir(images_folder) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print(f"❌ Nenhuma imagem encontrada em: {images_folder}")
        return
    
    print(f"🔍 Testando {len(image_files)} imagens...")
    
    total_detections = 0
    images_with_fire = 0
    
    # Test first 9 images for grid visualization
    sample_images = image_files[:9]
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    axes = axes.flatten()
    
    for i, img_file in enumerate(sample_images):
        img_path = os.path.join(images_folder, img_file)
        detections, results = test_single_image(model, img_path, conf_threshold)
        
        # Get annotated image
        annotated = results[0].plot()
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        
        # Display
        axes[i].imshow(annotated_rgb)
        axes[i].set_title(f"{img_file}\n{len(detections)} detections")
        axes[i].axis('off')
        
        # Update statistics
        if detections:
            total_detections += len(detections)
            images_with_fire += 1
            
        # Print summary for this image
        print(f"📸 {img_file}: {len(detections)} detections")
    
    plt.tight_layout()
    plt.show()
    
    # Overall statistics
    print(f"\n📊 ESTATÍSTICAS DO TESTE:")
    print(f"   Imagens testadas: {len(sample_images)}")
    print(f"   Imagens com detecção: {images_with_fire}")
    print(f"   Total de detecções: {total_detections}")
    print(f"   Média por imagem: {total_detections/len(sample_images):.1f}")

def validate_model_performance(model, dataset_path="datasets/wildfire"):
    """Validar performance do modelo no dataset"""
    
    data_yaml = os.path.join(dataset_path, "data.yaml")
    
    if not os.path.exists(data_yaml):
        print(f"❌ Dataset não encontrado: {data_yaml}")
        print("💡 Certifique-se que o dataset está na pasta correta")
        return
    
    print("🔄 Validando modelo no dataset...")
    
    # Run validation
    metrics = model.val(data=data_yaml)
    
    print(f"\n📈 MÉTRICAS DE VALIDAÇÃO:")
    print(f"   mAP50: {metrics.box.map50:.3f}")
    print(f"   mAP50-95: {metrics.box.map:.3f}")
    print(f"   Precision: {metrics.box.mp:.3f}")
    print(f"   Recall: {metrics.box.mr:.3f}")
    
    # Per-class metrics
    print(f"\n📋 MÉTRICAS POR CLASSE:")
    for class_id, class_name in model.names.items():
        if class_id < len(metrics.box.maps):
            print(f"   {class_name}: mAP50 = {metrics.box.maps[class_id]:.3f}")

def main():
    """Função principal de teste"""
    
    print("🔥 Teste do Modelo YOLOv8 Fire Detection")
    print("=" * 50)
    
    # Load model
    model_path = input("📂 Caminho do modelo (ou Enter para padrão): ").strip()
    if not model_path:
        model_path = "runs/detect/fire_detection_yolo/weights/best.pt"
    
    model = load_trained_model(model_path)
    if not model:
        return
    
    while True:
        print(f"\n🔧 OPÇÕES DE TESTE:")
        print("1. Testar imagem única")
        print("2. Testar pasta de imagens")
        print("3. Validar no dataset")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == "1":
            img_path = input("📷 Caminho da imagem: ").strip()
            conf = float(input("🎯 Threshold de confiança (0.1-1.0, padrão 0.5): ") or "0.5")
            
            detections, results = test_single_image(model, img_path, conf)
            if detections is not None:
                visualize_detection(img_path, detections, results)
        
        elif choice == "2":
            print("💡 Caminhos disponíveis:")
            print("   - datasets/wildfire/test/images (imagens de teste)")
            print("   - datasets/wildfire/train/images (imagens de treino)")
            print("   - datasets/wildfire/valid/images (imagens de validação)")
            folder_path = input("📁 Caminho da pasta: ").strip()
            
            # Auto-corrigir caminhos comuns
            if folder_path and not os.path.exists(folder_path):
                # Tentar adicionar datasets/ no início
                alt_path = f"datasets/{folder_path}"
                if os.path.exists(alt_path):
                    folder_path = alt_path
                    print(f"🔧 Usando caminho corrigido: {folder_path}")
            
            conf = float(input("🎯 Threshold de confiança (padrão 0.5): ") or "0.5")
            
            test_dataset_folder(model, folder_path, conf)
        
        elif choice == "3":
            dataset_path = input("📊 Caminho do dataset (padrão 'datasets/wildfire'): ").strip()
            if not dataset_path:
                dataset_path = "datasets/wildfire"
            
            validate_model_performance(model, dataset_path)
        
        elif choice == "4":
            print("👋 Até mais!")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
