#!/usr/bin/env python
"""
Script para verificar que los márgenes de precios están dentro del 10%
"""
import os
import sys
import django

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.base')
django.setup()

from apps.stock.ai_vehicle_generator import generar_vehiculos_con_ia
from apps.stock.scrapers import generar_datos_faltantes


def calcular_diferencia_porcentual(precio_venta, importe_compra):
    """Calcula la diferencia porcentual entre precio de venta y compra"""
    if precio_venta == 0:
        return 0
    diferencia = float(precio_venta) - float(importe_compra)
    porcentaje = (diferencia / float(precio_venta)) * 100
    return porcentaje


def verificar_margenes():
    print("=" * 80)
    print(" " * 25 + "🔍 VERIFICACIÓN DE MÁRGENES DE PRECIO")
    print("=" * 80)
    print()

    # Probar generación con IA
    print("🤖 PROBANDO GENERACIÓN CON IA...")
    print("-" * 80)

    try:
        vehiculos_ia = generar_vehiculos_con_ia(num_vehiculos=5)
        print(f"✅ Generados {len(vehiculos_ia)} vehículos con IA\n")

        margenes_fuera_limite = 0

        for i, vehiculo in enumerate(vehiculos_ia, 1):
            precio_venta = float(vehiculo.get('precio_venta', 0))
            importe_compra = float(vehiculo.get('importe_compra', 0))
            importe_costo = float(vehiculo.get('importe_costo', 0))

            dif_compra = calcular_diferencia_porcentual(precio_venta, importe_compra)
            dif_costo = calcular_diferencia_porcentual(precio_venta, importe_costo)

            print(f"🚗 VEHÍCULO {i}: {vehiculo.get('marca')} {vehiculo.get('modelo')}")
            print(f"   Precio Venta: {precio_venta:,.2f}€")
            print(f"   Importe Compra: {importe_compra:,.2f}€")
            print(f"   Importe Costo: {importe_costo:,.2f}€")
            print(f"   Diferencia Compra: {dif_compra:.2f}%", end="")

            if abs(dif_compra) > 10:
                print(" ❌ FUERA DE RANGO (>10%)")
                margenes_fuera_limite += 1
            else:
                print(" ✅ DENTRO DEL RANGO")

            print(f"   Diferencia Costo: {dif_costo:.2f}%", end="")

            if abs(dif_costo) > 10:
                print(" ❌ FUERA DE RANGO (>10%)")
                margenes_fuera_limite += 1
            else:
                print(" ✅ DENTRO DEL RANGO")

            print()

        print("-" * 80)
        if margenes_fuera_limite == 0:
            print("✅ TODOS LOS MÁRGENES ESTÁN DENTRO DEL 10%")
        else:
            print(f"❌ {margenes_fuera_limite} márgenes están fuera del límite del 10%")
        print()

    except Exception as e:
        print(f"❌ ERROR generando con IA: {str(e)}\n")


    # Probar generación aleatoria
    print("\n🎲 PROBANDO GENERACIÓN ALEATORIA...")
    print("-" * 80)

    margenes_fuera_limite_random = 0

    for i in range(1, 6):
        vehiculo = generar_datos_faltantes()

        precio_venta = float(vehiculo.get('precio_venta', 0))
        importe_compra = float(vehiculo.get('importe_compra', 0))
        importe_costo = float(vehiculo.get('importe_costo', 0))

        dif_compra = calcular_diferencia_porcentual(precio_venta, importe_compra)
        dif_costo = calcular_diferencia_porcentual(precio_venta, importe_costo)

        print(f"🚗 VEHÍCULO {i}: {vehiculo.get('marca')} {vehiculo.get('modelo')}")
        print(f"   Precio Venta: {precio_venta:,.2f}€")
        print(f"   Importe Compra: {importe_compra:,.2f}€")
        print(f"   Importe Costo: {importe_costo:,.2f}€")
        print(f"   Diferencia Compra: {dif_compra:.2f}%", end="")

        if abs(dif_compra) > 10:
            print(" ❌ FUERA DE RANGO (>10%)")
            margenes_fuera_limite_random += 1
        else:
            print(" ✅ DENTRO DEL RANGO")

        print(f"   Diferencia Costo: {dif_costo:.2f}%", end="")

        if abs(dif_costo) > 10:
            print(" ❌ FUERA DE RANGO (>10%)")
            margenes_fuera_limite_random += 1
        else:
            print(" ✅ DENTRO DEL RANGO")

        print()

    print("-" * 80)
    if margenes_fuera_limite_random == 0:
        print("✅ TODOS LOS MÁRGENES ESTÁN DENTRO DEL 10%")
    else:
        print(f"❌ {margenes_fuera_limite_random} márgenes están fuera del límite del 10%")

    print("\n" + "=" * 80)
    print(" " * 30 + "📊 RESUMEN FINAL")
    print("=" * 80)
    print(f"Total vehículos probados: 10")
    print(f"Márgenes fuera de límite (IA): {margenes_fuera_limite}")
    print(f"Márgenes fuera de límite (Aleatorio): {margenes_fuera_limite_random}")

    if margenes_fuera_limite == 0 and margenes_fuera_limite_random == 0:
        print("\n✅ ¡VERIFICACIÓN EXITOSA! Todos los márgenes están dentro del 10%")
    else:
        print(f"\n⚠️  VERIFICACIÓN PARCIAL: {margenes_fuera_limite + margenes_fuera_limite_random} márgenes fuera de límite")

    print("=" * 80)


if __name__ == "__main__":
    verificar_margenes()
