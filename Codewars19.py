def isDigit(s):
  s = s.strip()
  try:
      float(s)
      return True
  except ValueError:
      return False
