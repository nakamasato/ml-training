import ray
ray.init('ray://head_node_ip_address>:10001')

@ray.remote
def f(x):
    return x * x

futures = [f.remote(i) for i in range(4)]
print(ray.get(futures))
