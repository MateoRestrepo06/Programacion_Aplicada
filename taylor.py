def logaritmo(x, max_iter=100):
  if x <= 0:
      raise ValueError("El logaritmo natural está definido solo para x mayores que 0.")

  z = x - 1
  acc = 0
  p = z
  sign = 1

  for n in range(1, max_iter + 1):
      term = sign * p / n
      acc += term

      p *= z
      sign = -sign
  return acc
