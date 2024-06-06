from datetime import datetime, timedelta

fecha_inicial = datetime(year=2023, month=3, day=6)

fecha_final = datetime(2023, 7, 1)

print(f"La cantidad de días entre medio es de {(fecha_final - fecha_inicial).days}")