def most_frequent_item_count(arr):
  if len(arr) == 0:
      return 0
  return max(arr.count(x) for x in arr)
