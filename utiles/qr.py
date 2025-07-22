import qrcode
from PIL import Image

# Datos de la red Wi-Fi
ssid = "TGD_InSSSeP"
password = "notieneclave"
security_type = "WPA"  # Puedes cambiarlo a 'WEP' o 'nopass' si es necesario

# Formato estándar para QR WiFi
wifi_qr_data = f"WIFI:T:{security_type};S:{ssid};P:{password};;"

# Generar QR
qr = qrcode.make(wifi_qr_data)

# Guardar imagen temporal para mostrar
qr_path = "/home/sambu/Proyectos/Vete_001/utiles/wifi_qr_tgd_insssep.png"
qr.save(qr_path)

qr.show()
qr_path