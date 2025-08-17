"""
Script para testar a API QueimadAI
Testa todos os endpoints com arquivos de exemplo
"""

import requests
import json
import os
import time
from pathlib import Path

API_BASE = "http://localhost:3000"

def test_health_check():
    """Testa o health check da API"""
    print("🔍 Testando Health Check...")
    try:
        response = requests.get(f"{API_BASE}/api/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            data = response.json()
            print(f"   Status: {data.get('message', 'Unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se que ela está rodando em localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_detection_status():
    """Testa o status do serviço de detecção"""
    print("\n🔍 Testando Detection Status...")
    try:
        response = requests.get(f"{API_BASE}/api/detect/status")
        if response.status_code == 200:
            print("✅ Detection status OK")
            data = response.json()
            if data.get('success'):
                status_info = data.get('data', {})
                print(f"   Service: {status_info.get('service', 'Unknown')}")
                print(f"   Status: {status_info.get('status', 'Unknown')}")
                print(f"   Model loaded: {status_info.get('model_loaded', False)}")
                return True
        else:
            print(f"❌ Detection status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no detection status: {e}")
        return False

def create_test_image():
    """Cria uma imagem de teste simples se não existir"""
    test_image_path = "test_image.jpg"
    
    if os.path.exists(test_image_path):
        return test_image_path
    
    try:
        # Criar uma imagem simples com PIL se disponível
        from PIL import Image, ImageDraw
        import numpy as np
        
        # Criar imagem 400x300 com gradient vermelho/laranja (simula fogo)
        img = Image.new('RGB', (400, 300), color='black')
        draw = ImageDraw.Draw(img)
        
        # Desenhar "fogo" simples
        draw.ellipse([100, 150, 300, 250], fill='red')
        draw.ellipse([120, 170, 280, 230], fill='orange')
        draw.ellipse([140, 180, 260, 220], fill='yellow')
        
        img.save(test_image_path)
        print(f"✅ Imagem de teste criada: {test_image_path}")
        return test_image_path
        
    except ImportError:
        print("⚠️  PIL não disponível. Crie manualmente um arquivo 'test_image.jpg' para testar")
        return None

def test_image_detection():
    """Testa detecção em imagem"""
    print("\n🔍 Testando Image Detection...")
    
    # Criar ou usar imagem de teste
    test_image = create_test_image()
    
    if not test_image or not os.path.exists(test_image):
        print("❌ Arquivo de teste não encontrado. Crie um arquivo 'test_image.jpg' para testar")
        return False
    
    try:
        with open(test_image, 'rb') as f:
            files = {'image': f}
            
            print(f"📤 Enviando imagem: {test_image}")
            start_time = time.time()
            
            response = requests.post(f"{API_BASE}/api/detect/image", files=files)
            
            end_time = time.time()
            
            if response.status_code == 200:
                print("✅ Image detection OK")
                data = response.json()
                
                if data.get('success'):
                    result = data.get('data', {})
                    print(f"   Fire detected: {result.get('fire_detected', False)}")
                    print(f"   Confidence: {result.get('confidence', 0)}")
                    print(f"   Bounding boxes: {len(result.get('bounding_boxes', []))}")
                    print(f"   Processing time: {result.get('metadata', {}).get('processing_time', 'Unknown')}")
                    print(f"   API response time: {end_time - start_time:.2f}s")
                    
                    # Mostrar bounding boxes se existirem
                    for i, bbox in enumerate(result.get('bounding_boxes', [])):
                        print(f"   Box {i+1}: ({bbox.get('x', 0)}, {bbox.get('y', 0)}) "
                              f"{bbox.get('width', 0)}x{bbox.get('height', 0)} "
                              f"[{bbox.get('class', 'unknown')}] "
                              f"conf: {bbox.get('confidence', 0)}")
                    
                    return True
                else:
                    print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Image detection failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Erro no image detection: {e}")
        return False

def test_detection_stats():
    """Testa estatísticas de detecção"""
    print("\n🔍 Testando Detection Stats...")
    try:
        response = requests.get(f"{API_BASE}/api/detect/stats")
        if response.status_code == 200:
            print("✅ Detection stats OK")
            data = response.json()
            if data.get('success'):
                stats = data.get('data', {})
                print(f"   Total detections: {stats.get('total_detections', 0)}")
                print(f"   Fire detections: {stats.get('fire_detections', 0)}")
                print(f"   Image detections: {stats.get('image_detections', 0)}")
                print(f"   Video detections: {stats.get('video_detections', 0)}")
                print(f"   Avg fire confidence: {stats.get('avg_fire_confidence', 0):.3f}")
                print(f"   Avg processing time: {stats.get('avg_processing_time', 0):.1f}ms")
                return True
        else:
            print(f"❌ Detection stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no detection stats: {e}")
        return False

def test_detection_history():
    """Testa histórico de detecções"""
    print("\n🔍 Testando Detection History...")
    try:
        response = requests.get(f"{API_BASE}/api/detect/history?limit=5")
        if response.status_code == 200:
            print("✅ Detection history OK")
            data = response.json()
            if data.get('success'):
                history = data.get('data', [])
                print(f"   Retrieved {len(history)} records")
                for i, record in enumerate(history[:3]):  # Show first 3
                    print(f"   {i+1}. {record.get('original_filename', 'unknown')} - "
                          f"Fire: {record.get('fire_detected', False)} "
                          f"({record.get('confidence', 0):.3f})")
                return True
        else:
            print(f"❌ Detection history failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no detection history: {e}")
        return False

def test_video_detection():
    """Testa detecção em vídeo (se houver arquivo de teste)"""
    print("\n🔍 Testando Video Detection...")
    
    # Procurar por arquivos de vídeo de teste
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    test_video = None
    
    for ext in video_extensions:
        for filename in [f'test_video{ext}', f'sample{ext}', f'video_test{ext}']:
            if os.path.exists(filename):
                test_video = filename
                break
        if test_video:
            break
    
    if not test_video:
        print("⚠️  Nenhum vídeo de teste encontrado (test_video.mp4, sample.mp4, etc.)")
        print("   Crie um arquivo de vídeo para testar esta funcionalidade")
        return True  # Não é erro crítico
    
    try:
        with open(test_video, 'rb') as f:
            files = {'video': f}
            
            print(f"📤 Enviando vídeo: {test_video}")
            start_time = time.time()
            
            response = requests.post(f"{API_BASE}/api/detect/video", files=files)
            
            end_time = time.time()
            
            if response.status_code == 200:
                print("✅ Video detection OK")
                data = response.json()
                
                if data.get('success'):
                    result = data.get('data', {})
                    print(f"   Total frames: {result.get('total_frames', 0)}")
                    print(f"   Frames with fire: {result.get('frames_with_fire', 0)}")
                    print(f"   Fire detected: {result.get('fire_detected', False)}")
                    print(f"   Overall confidence: {result.get('overall_confidence', 0)}")
                    print(f"   API response time: {end_time - start_time:.2f}s")
                    
                    return True
                else:
                    print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Video detection failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Erro no video detection: {e}")
        return False
    """Testa detecção em vídeo (se houver arquivo de teste)"""
    print("\n🔍 Testando Video Detection...")
    
    # Procurar por arquivos de vídeo de teste
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    test_video = None
    
    for ext in video_extensions:
        for filename in [f'test_video{ext}', f'sample{ext}', f'video_test{ext}']:
            if os.path.exists(filename):
                test_video = filename
                break
        if test_video:
            break
    
    if not test_video:
        print("⚠️  Nenhum vídeo de teste encontrado (test_video.mp4, sample.mp4, etc.)")
        print("   Crie um arquivo de vídeo para testar esta funcionalidade")
        return True  # Não é erro crítico
    
    try:
        with open(test_video, 'rb') as f:
            files = {'video': f}
            
            print(f"📤 Enviando vídeo: {test_video}")
            start_time = time.time()
            
            response = requests.post(f"{API_BASE}/api/detect/video", files=files)
            
            end_time = time.time()
            
            if response.status_code == 200:
                print("✅ Video detection OK")
                data = response.json()
                
                if data.get('success'):
                    result = data.get('data', {})
                    print(f"   Total frames: {result.get('total_frames', 0)}")
                    print(f"   Frames with fire: {result.get('frames_with_fire', 0)}")
                    print(f"   Fire detected: {result.get('fire_detected', False)}")
                    print(f"   Overall confidence: {result.get('overall_confidence', 0)}")
                    print(f"   API response time: {end_time - start_time:.2f}s")
                    
                    return True
                else:
                    print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Video detection failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Erro no video detection: {e}")
        return False

def main():
    print("🔥 QueimadAI API Test Suite")
    print("=" * 50)
    
    # Lista de testes
    tests = [
        ("Health Check", test_health_check),
        ("Detection Status", test_detection_status),
        ("Image Detection", test_image_detection),
        ("Detection Stats", test_detection_stats),
        ("Detection History", test_detection_history),
        ("Video Detection", test_video_detection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("🎉 Todos os testes passaram! API está funcionando perfeitamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
    
    return passed == len(results)

if __name__ == "__main__":
    main()
