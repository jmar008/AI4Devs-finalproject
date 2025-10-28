"""
Script maestro para generar todos los datos iniciales del sistema DealaAI
Genera en orden: Provincias -> Concesionarios -> Usuarios -> Perfiles -> Vehículos
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.development')
django.setup()

from django.core.management import call_command
from colorama import Fore, Style, init

# Inicializar colorama para colores en consola
init(autoreset=True)

def print_header(mensaje):
    """Imprime un encabezado destacado"""
    print("\n" + "="*70)
    print(f"{Fore.CYAN}{Style.BRIGHT}{mensaje}")
    print("="*70 + "\n")

def print_success(mensaje):
    """Imprime un mensaje de éxito"""
    print(f"{Fore.GREEN}✅ {mensaje}{Style.RESET_ALL}")

def print_info(mensaje):
    """Imprime un mensaje informativo"""
    print(f"{Fore.YELLOW}ℹ️  {mensaje}{Style.RESET_ALL}")

def print_error(mensaje):
    """Imprime un mensaje de error"""
    print(f"{Fore.RED}❌ {mensaje}{Style.RESET_ALL}")

def generar_todos_los_datos():
    """
    Genera todos los datos del sistema en el orden correcto
    """
    try:
        print_header("🚀 GENERACIÓN COMPLETA DE DATOS - DealaAI")
        print_info("Este proceso generará todos los datos necesarios para el sistema")
        print_info("Orden: Provincias → Concesionarios → Usuarios → Perfiles → Vehículos\n")

        # 1. Generar Provincias
        print_header("📍 PASO 1/5: Generando Provincias de España")
        try:
            call_command('generar_provincias_solo')
            print_success("49 provincias generadas correctamente")
        except Exception as e:
            print_error(f"Error generando provincias: {e}")
            return False

        # 2. Generar Concesionarios
        print_header("🏢 PASO 2/5: Generando Concesionarios")
        try:
            call_command('generar_concesionarios')
            print_success("Concesionarios generados correctamente")
        except Exception as e:
            print_error(f"Error generando concesionarios: {e}")
            return False

        # 3. Generar Usuarios
        print_header("👥 PASO 3/5: Generando Usuarios Jerárquicos")
        print_info("Generando estructura organizacional completa...")
        try:
            call_command('generar_usuarios_completos', '--no-borrar-admin')
            print_success("46 usuarios generados con jerarquía organizacional")
        except Exception as e:
            print_error(f"Error generando usuarios: {e}")
            return False

        # 4. Generar Perfiles
        print_header("📋 PASO 4/5: Generando Perfiles de Usuario")
        print_info("Creando perfiles asociados a usuarios...")
        try:
            from apps.authentication.models import User, Profile
            usuarios_sin_perfil = User.objects.filter(perfil__isnull=True)
            count = 0
            for user in usuarios_sin_perfil:
                if not hasattr(user, 'perfil'):
                    Profile.objects.create(
                        user=user,
                        empresa="DealaAI",
                        puesto=user.puesto or "Empleado",
                        sector="Automoción"
                    )
                    count += 1
            print_success(f"{count} perfiles generados correctamente")
        except Exception as e:
            print_error(f"Error generando perfiles: {e}")
            return False

        # 5. Generar Vehículos con IA
        print_header("🚗 PASO 5/5: Generando 100 Vehículos con IA")
        print_info("Usando modelo openai/gpt-oss-20b para generar datos realistas...")
        print_info("Este proceso puede tardar unos minutos...\n")
        try:
            call_command(
                'migrate_stock_and_scrape',
                '--usar-ia',
                '--cantidad', '100'
            )
            print_success("100 vehículos generados con IA correctamente")
        except Exception as e:
            print_error(f"Error generando vehículos: {e}")
            return False

        # Resumen final
        print_header("✨ GENERACIÓN COMPLETADA EXITOSAMENTE")
        print_success("Todos los datos se generaron correctamente:")
        print(f"{Fore.CYAN}  📍 49 Provincias")
        print(f"{Fore.CYAN}  🏢 Concesionarios por provincia")
        print(f"{Fore.CYAN}  👥 46 Usuarios jerárquicos")
        print(f"{Fore.CYAN}  📋 Perfiles de usuario")
        print(f"{Fore.CYAN}  🚗 100 Vehículos con datos IA")
        print("\n" + "="*70)
        print(f"{Fore.GREEN}{Style.BRIGHT}🎉 Sistema listo para usar!")
        print("="*70 + "\n")

        return True

    except KeyboardInterrupt:
        print_error("\n\n⚠️  Proceso cancelado por el usuario")
        return False
    except Exception as e:
        print_error(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generar_todos_los_datos()
    sys.exit(0 if success else 1)
