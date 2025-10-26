#!/usr/bin/env python
"""
Script para verificar qué modelos de OpenRouter están disponibles
Prueba cada modelo de la configuración y muestra su estado
"""
import os
import sys
import django

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.base')
django.setup()

from django.conf import settings
from openai import OpenAI
import httpx


def verificar_modelos():
    """Verifica la disponibilidad de cada modelo configurado"""

    print("=" * 100)
    print(" " * 30 + "🔍 VERIFICACIÓN DE MODELOS OPENROUTER")
    print("=" * 100)
    print()

    # Cliente httpx con SSL deshabilitado para Zscaler
    http_client = httpx.Client(verify=False)

    client = OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_API_BASE,
        http_client=http_client,
    )

    # Lista de todos los modelos a verificar
    modelos = [settings.DEEPSEEK_MODEL] + settings.DEEPSEEK_FALLBACK_MODELS

    print(f"📋 Total de modelos a verificar: {len(modelos)}")
    print()
    print("-" * 100)

    modelos_disponibles = []
    modelos_no_disponibles = []

    for i, modelo in enumerate(modelos, 1):
        print(f"\n{i}. Probando: {modelo}")
        print("   ", end="", flush=True)

        try:
            # Hacer una llamada simple de prueba
            response = client.chat.completions.create(
                model=modelo,
                messages=[
                    {
                        "role": "user",
                        "content": "Responde solo con 'OK'"
                    }
                ],
                max_tokens=10,
                temperature=0.1,
                extra_body={
                    "data_collection": "allow"
                }
            )

            print(f"✅ DISPONIBLE")
            print(f"   Respuesta: {response.choices[0].message.content[:50]}")
            print(f"   Tokens: {response.usage.total_tokens}")
            modelos_disponibles.append(modelo)

        except Exception as e:
            error_str = str(e)

            if "404" in error_str or "not found" in error_str.lower():
                print(f"❌ NO DISPONIBLE (404 - Modelo no encontrado)")
                modelos_no_disponibles.append((modelo, "404 - No encontrado"))
            elif "429" in error_str or "rate" in error_str.lower():
                print(f"⚠️  RATE LIMIT (pero el modelo existe)")
                print(f"   Error: {error_str[:100]}")
                modelos_disponibles.append(modelo)  # Existe pero con rate limit
            else:
                print(f"❌ ERROR: {error_str[:100]}")
                modelos_no_disponibles.append((modelo, error_str[:100]))

    # Resumen
    print()
    print("=" * 100)
    print(" " * 35 + "📊 RESUMEN")
    print("=" * 100)
    print()
    print(f"✅ Modelos disponibles: {len(modelos_disponibles)}/{len(modelos)}")
    print(f"❌ Modelos no disponibles: {len(modelos_no_disponibles)}/{len(modelos)}")
    print()

    if modelos_disponibles:
        print("✅ MODELOS DISPONIBLES:")
        print("-" * 100)
        for modelo in modelos_disponibles:
            print(f"   • {modelo}")
        print()

    if modelos_no_disponibles:
        print("❌ MODELOS NO DISPONIBLES:")
        print("-" * 100)
        for modelo, error in modelos_no_disponibles:
            print(f"   • {modelo}")
            print(f"     Razón: {error}")
        print()

    # Recomendaciones
    if modelos_no_disponibles:
        print("💡 RECOMENDACIÓN:")
        print("   Actualiza settings.py eliminando estos modelos:")
        print()
        print("   DEEPSEEK_FALLBACK_MODELS = [")
        for modelo in modelos_disponibles[1:]:  # Excluir modelo principal
            print(f"       '{modelo}',")
        print("   ]")
        print()

    print("=" * 100)


if __name__ == "__main__":
    try:
        verificar_modelos()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()
