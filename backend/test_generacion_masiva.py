#!/usr/bin/env python
"""
Script de prueba para generación masiva de vehículos (>1000)
Demuestra la capacidad del sistema con múltiples modelos fallback
"""
import os
import sys
import django
import time
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.base')
django.setup()

from apps.stock.ai_vehicle_generator import generar_vehiculos_con_ia
from django.conf import settings


def test_generacion_masiva(cantidad=100):
    """Prueba la generación masiva de vehículos"""

    print("=" * 100)
    print(f" " * 30 + f"🚀 GENERACIÓN MASIVA: {cantidad} VEHÍCULOS")
    print("=" * 100)
    print()

    print("📋 CONFIGURACIÓN:")
    print(f"   Modelo Principal: {settings.DEEPSEEK_MODEL}")
    print(f"   Modelos Fallback: {len(settings.DEEPSEEK_FALLBACK_MODELS)} modelos")
    print(f"   Total Modelos: {1 + len(settings.DEEPSEEK_FALLBACK_MODELS)} modelos")
    print()

    print("🤖 MODELOS DISPONIBLES:")
    print(f"   1. {settings.DEEPSEEK_MODEL} (principal)")
    for i, modelo in enumerate(settings.DEEPSEEK_FALLBACK_MODELS, 2):
        print(f"   {i}. {modelo}")
    print()

    print("-" * 100)
    print(f"⏱️  INICIANDO GENERACIÓN DE {cantidad} VEHÍCULOS...")
    print("-" * 100)
    print()

    inicio = time.time()

    try:
        vehiculos = generar_vehiculos_con_ia(num_vehiculos=cantidad)

        fin = time.time()
        tiempo_total = fin - inicio

        print()
        print("=" * 100)
        print(" " * 35 + "📊 RESULTADOS")
        print("=" * 100)
        print()
        print(f"✅ Vehículos generados: {len(vehiculos)}")
        print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
        print(f"⚡ Velocidad: {len(vehiculos) / tiempo_total:.2f} vehículos/segundo")
        print(f"📈 Tasa de éxito: {(len(vehiculos) / cantidad) * 100:.1f}%")
        print()

        # Mostrar algunos ejemplos
        print("🚗 EJEMPLOS DE VEHÍCULOS GENERADOS:")
        print("-" * 100)

        for i, vehiculo in enumerate(vehiculos[:5], 1):
            marca = vehiculo.get('marca', 'N/A')
            modelo = vehiculo.get('modelo', 'N/A')
            anio = vehiculo.get('anio_matricula', 'N/A')
            km = vehiculo.get('kilometros', 0)
            precio = vehiculo.get('precio_venta', 0)
            compra = vehiculo.get('importe_compra', 0)

            # Calcular margen
            if precio > 0:
                margen = ((float(precio) - float(compra)) / float(precio)) * 100
            else:
                margen = 0

            print(f"   {i}. {marca} {modelo} ({anio}) - {km:,} km")
            print(f"      Precio: {precio}€ | Compra: {compra}€ | Margen: {margen:.1f}%")

        if len(vehiculos) > 5:
            print(f"   ... y {len(vehiculos) - 5} vehículos más")

        print()
        print("=" * 100)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 100)

    except Exception as e:
        print()
        print("=" * 100)
        print("❌ ERROR EN LA GENERACIÓN")
        print("=" * 100)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


def menu():
    """Menú interactivo para seleccionar cantidad"""
    print("=" * 100)
    print(" " * 30 + "🎯 PRUEBA DE GENERACIÓN MASIVA CON IA")
    print("=" * 100)
    print()
    print("Selecciona la cantidad de vehículos a generar:")
    print()
    print("   1. 50 vehículos (prueba rápida)")
    print("   2. 100 vehículos (prueba normal)")
    print("   3. 500 vehículos (generación grande)")
    print("   4. 1000 vehículos (generación masiva)")
    print("   5. Cantidad personalizada")
    print("   0. Salir")
    print()

    opcion = input("Opción: ").strip()

    if opcion == "1":
        test_generacion_masiva(50)
    elif opcion == "2":
        test_generacion_masiva(100)
    elif opcion == "3":
        test_generacion_masiva(500)
    elif opcion == "4":
        test_generacion_masiva(1000)
    elif opcion == "5":
        try:
            cantidad = int(input("Cantidad de vehículos: ").strip())
            if cantidad > 0:
                test_generacion_masiva(cantidad)
            else:
                print("❌ La cantidad debe ser mayor a 0")
        except ValueError:
            print("❌ Cantidad inválida")
    elif opcion == "0":
        print("👋 Saliendo...")
    else:
        print("❌ Opción inválida")


if __name__ == "__main__":
    # Si se pasa un argumento numérico, usarlo como cantidad
    if len(sys.argv) > 1:
        try:
            cantidad = int(sys.argv[1])
            test_generacion_masiva(cantidad)
        except ValueError:
            print("❌ Argumento inválido. Uso: python test_generacion_masiva.py [cantidad]")
    else:
        menu()
