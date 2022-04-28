import ray
import numpy as np

@ray.remote
def map(obj, f):
    return f(obj)
@ray.remote
def sum_results(*elements):
    return np.sum(elements)

items = list(range(100))
map_func = lambda i : i*2
remote_elements = [map.remote(i, map_func) for i in items]

# simple reduce
remote_final_sum = sum_results.remote(*remote_elements)
result = ray.get(remote_final_sum)
print(result)

# tree reduce
intermediate_results = [sum_results.remote(
    *remote_elements[i * 20: (i + 1) * 20]) for i in range(5)]
remote_final_sum = sum_results.remote(*intermediate_results)
result = ray.get(remote_final_sum)
print(result)
