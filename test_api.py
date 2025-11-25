import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/auth'

def print_response(response, title):
    print(f"\n--- {title} ---")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def run_tests():
    # 1. Registrar un Proveedor (KunaPet Vet)
    provider_data = {
        "email": "veterinaria@kunapet.com",
        "password": "TestPassword123!",
        "business_name": "KunaPet Veterinaria",
        "ruc": "20123456789",
        "address": "Av. Principal 123",
        "phone": "999888777",
        "bio": "Especialistas en perros y gatos"
    }
    
    print("1. Intentando registrar Proveedor...")
    res = requests.post(f"{BASE_URL}/register/provider/", json=provider_data)
    print_response(res, "Registro Proveedor")

    # 2. Intentar Login con ese usuario
    login_data = {
        "email": "veterinaria@kunapet.com",
        "password": "TestPassword123!"
    }
    
    print("\n2. Intentando Login...")
    res = requests.post(f"{BASE_URL}/login/", json=login_data)
    print_response(res, "Login")

    if res.status_code == 200:
        token = res.json()['access']
        
        # 3. Obtener datos del perfil (Me)
        headers = {'Authorization': f'Bearer {token}'}
        print("\n3. Obteniendo Perfil (/me)...")
        res = requests.get(f"{BASE_URL}/me/", headers=headers)
        print_response(res, "Mi Perfil")
    else:
        print("\nSkipping profile check due to login failure.")

if __name__ == "__main__":
    # Asegúrate de tener 'requests' instalado: pip install requests
    try:
        run_tests()
    except ImportError:
        print("Por favor instala requests: pip install requests")
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de que el servidor esté corriendo en otra terminal.")
