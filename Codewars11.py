def get_size(length, width, height):
  surface_area = 2 * (length * width + width * height + height * length)
  volume = length * width * height
  return [surface_area, volume]
