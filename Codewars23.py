def weather_info(fahrenheit):
  celsius = (fahrenheit - 32) * (5 / 9)
  if celsius > 0:
      return f"{celsius:.1f} is above freezing temperature"
  else:
      return f"{celsius:.1f} is freezing temperature"
