#!/usr/bin/env python
"""
Script de prueba para el generador de vehículos con IA
Genera vehículos de ejemplo y muestra los datos generados
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.base')
django.setup()

from apps.stock.ai_vehicle_generator import generar_vehiculos_con_ia
import json


def main():
    print("=" * 80)
    print("🤖 GENERADOR DE VEHÍCULOS CON IA - PRUEBA")
    print("=" * 80)
    print()

    # Prueba 1: Generar 3 vehículos de cualquier marca
    print("📊 PRUEBA 1: Generando 3 vehículos de marcas variadas...")
    print("-" * 80)

    try:
        vehiculos = generar_vehiculos_con_ia(num_vehiculos=3)

        for i, vehiculo in enumerate(vehiculos, 1):
            print(f"\n🚗 VEHÍCULO {i}:")
            print(f"   Marca/Modelo: {vehiculo.get('marca', 'N/A')} {vehiculo.get('modelo', 'N/A')}")
            print(f"   Versión: {vehiculo.get('version', 'N/A')}")
            print(f"   Año: {vehiculo.get('anio_matricula', 'N/A')}")
            print(f"   Kilometraje: {vehiculo.get('kilometros', 'N/A'):,} km")
            print(f"   Precio: {vehiculo.get('precio_venta', 'N/A')}€")
            print(f"   Color: {vehiculo.get('color', 'N/A')}")
            print(f"   Combustible: {vehiculo.get('combustible', 'N/A')}")
            print(f"   Transmisión: {vehiculo.get('transmision', 'N/A')}")
            print(f"   Potencia: {vehiculo.get('potencia', 'N/A')} CV")
            print(f"   Días en stock: {vehiculo.get('dias_stock', 'N/A')}")
            print(f"   Coste compra: {vehiculo.get('importe_compra', 'N/A')}€")

        print("\n" + "=" * 80)
        print("✅ PRUEBA COMPLETADA")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


    # Prueba 2: Generar vehículos de marca específica
    print("\n\n📊 PRUEBA 2: Generando 2 vehículos BMW...")
    print("-" * 80)

    try:
        vehiculos_bmw = generar_vehiculos_con_ia(num_vehiculos=2, marca="BMW")

        for i, vehiculo in enumerate(vehiculos_bmw, 1):
            print(f"\n🚗 BMW {i}:")
            print(f"   Modelo completo: {vehiculo.get('marca', 'N/A')} {vehiculo.get('modelo', 'N/A')} {vehiculo.get('version', 'N/A')}")
            print(f"   Año/KM: {vehiculo.get('anio_matricula', 'N/A')} / {vehiculo.get('kilometros', 'N/A'):,} km")
            print(f"   Precio: {vehiculo.get('precio_venta', 'N/A')}€")

        print("\n" + "=" * 80)
        print("✅ PRUEBA COMPLETADA")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
