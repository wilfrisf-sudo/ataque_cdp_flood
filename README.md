Laboratorio de Seguridad: Ataque DoS mediante Inundación CDP
-----------------------------------------------------------------------------------------------------------------------
Autor: Wilfri Solano Frias
Matrícula: 2024-2364
-----------------------------------------------------------------------------------------------------------------------
1. Objetivo del Laboratorio
Conocer las vulnerabilidades y peligros reales de los protocolos de descubrimiento no autenticados en entornos LAN, analizando cómo la falta de seguridad puede ser explotada para desestabilizar la infraestructura física.
-----------------------------------------------------------------------------------------------------------------------
2. Objetivo del Script
Inyectar miles de identidades falsas (`Cisco-Falso-X`) a alta velocidad para saturar el proceso Cisco Discovery Protocol (CDP) y congelar la administración (plano de control) del switch.

2.1. Requisitos para utilizar la herramienta
* Sistema Operativo: Kali Linux.

* Lenguaje: Python 3.x.
  
* Librerías/Dependencias:** capy (con el submódulo `scapy.contrib.cdp`). Instalar con: `pip install scapy`. También es obligatorio tener el binario del sistema `tcpreplay` instalado (`sudo apt install tcpreplay`).

* Entorno de Red: Acceso a la interfaz de red local en modo promiscuo y ejecución del script con privilegios de administrador (root).

2.2. Parámetros Usados
El script admite y manipula las siguientes variables y configuraciones:
* `MI_INTERFAZ_RED`: Interfaz física o virtual del atacante conectada al segmento bajo prueba (ej. `eth0`).
* `CANTIDAD_A_ENVIAR`: Volumen total de tramas maliciosas a inyectar (fijado en 8,000 tramas).
* `mac_origen`: Dirección física forjada de manera incremental bit a bit para evitar colisiones y simular hosts únicos.
* `nombre_dispositivo`: Identificador único del host (`Cisco-Falso-X`) diseñado para saturar la memoria del switch.
* `puerto_origen`: Distribución cíclica de interfaces ficticias (`GigabitEthernet0/0` a `0/23`).
* `pps=50000`: Argumento del método `sendpfast` que delega el envío a `tcpreplay` para garantizar una transferencia masiva.
-----------------------------------------------------------------------------------------------------------------------
3. Documentación del Funcionamiento del Script
El programa crea una lista en la memoria RAM del atacante que precarga 8,000 estructuras lógicas CDP válidas (con cabeceras LLC y SNAP). Cada paquete varía su dirección MAC de origen y su *Device ID* interno. Una vez construidos, el script invoca a `sendpfast`, transmitiendo la totalidad de los paquetes a una velocidad de 50,000 tramas por segundo. Al ser un switch virtual (IOU) sin chips ASIC físicos de Capa 2, debe procesar cada paquete falso mediante interrupciones de software (CPU), lo que inhabilita instantáneamente la respuesta de la consola de comandos debido a la sobrecarga.
-----------------------------------------------------------------------------------------------------------------------
4. Documentación de la Red
4.1. Topología
* Descripción: Infraestructura virtualizada en GNS3 compuesta por un Router legítimo (para probar la función natural de CDP), un Switch de Acceso bajo prueba (SWI2) y la estación del atacante.
* VLANs Configuradas: VLAN 1 (Nativa / Por defecto).
* Direccionamiento IP:
  * Segmento de Red: `192.168.124.0` / `255.255.255.0`
  * Atacante (Kali Linux): `192.168.124.135` / `255.255.255.0`
* Interfaces Clave:
  * `Ethernet0/0` (SWI2) apuntando al Router.
  * `Ethernet0/1` (SWI2) apuntando al host atacante (Kali).
-----------------------------------------------------------------------------------------------------------------------
5. Contramedidas (Mitigación)
Para anular este vector de ataque y proteger la estabilidad del Switch Cisco, se aplican las siguientes directivas en el IOS:

A. Desactivación Selectiva por Interfaz (Recomendada en Acceso):
Consiste en apagar CDP únicamente en los puertos donde se conectan usuarios o sistemas finales (como el puerto del atacante), manteniéndolo en los enlaces troncales.
SWI2# configure terminal
SWI2(config)# interface Ethernet0/1
SWI2(config-if)# no cdp enable
SWI2(config-if)# end

B.Desactivación Global del Protocolo:
Si la infraestructura no depende de estas herramientas de descubrimiento ni utiliza telefonía IP, se recomienda apagarlo por completo.
SWI2# configure terminal
SWI2(config)# no cdp run
SWI2(config)# end
-----------------------------------------------------------------------------------------------------------------------
6. Evidencias
7. 
6.1. Demostración en Video

En el siguiente enlace se encuentra el video demostrativo donde se visualiza la topología con la ejecución del ataque y la aplicación de la contramedida:

https://youtu.be/L43TLI6w06o?si=EQB0W8h4c1NpTNgM

6.2. Capturas de Pantalla
Topología en GNS3

<img width="414" height="379" alt="imagen" src="https://github.com/user-attachments/assets/ba9d7946-e55e-468b-a482-3a6d5752f6af" />

Estado normal

<img width="827" height="233" alt="imagen" src="https://github.com/user-attachments/assets/7011bfdd-fa99-4671-a068-4155fe4e5bd4" />

Ejecución del script

<img width="427" height="360" alt="imagen" src="https://github.com/user-attachments/assets/8a11f4f3-60a8-42f3-87e1-e43cc0809850" />

Impacto en el switch

<img width="651" height="441" alt="imagen" src="https://github.com/user-attachments/assets/f9836c05-34ab-47fb-b1af-0f1f6a32f49b" />

Aplicación de contramedidas

<img width="443" height="68" alt="imagen" src="https://github.com/user-attachments/assets/959efb2f-5a4c-4962-9e1b-b792b4fcf03c" />
