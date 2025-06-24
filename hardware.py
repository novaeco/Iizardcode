# hardware.py


def send_serial_command(cmd, baud=115200):
    """Send a command to the first detected serial port."""
    try:
        import serial.tools.list_ports

        ports = list(serial.tools.list_ports.comports())
        if not ports:
            print("Aucun port COM détecté.")
            return False
        port = ports[0].device
        import serial

        with serial.Serial(port, baud, timeout=2) as ser:
            ser.write((cmd + "\n").encode("utf-8"))
        print(f"Commande envoyée à {port} : {cmd}")
        return True
    except Exception as e:
        print(f"Erreur envoi série : {e}")
        return False
