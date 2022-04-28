import ray
import time
import numpy as np

@ray.remote
class Actor:
    def heavy_compute(self, large_array):
        # taking a long time...
        time.sleep(0.1)


actor = Actor.remote()
result_refs = []
MAX_NUM_IN_FLIGHT = 1000
for i in range(1_000_000):
    large_array = np.zeros(1_000_000)

    # Allow 1000 in flight calls
    # For example, if i = 5000, this call blocks until that
    # 4000 of the object_refs in result_refs are ready
    # and available.
    if len(result_refs) > MAX_NUM_IN_FLIGHT:
        num_ready = i-MAX_NUM_IN_FLIGHT
        ray.wait(result_refs, num_returns=num_ready)

    result_refs.append(actor.heavy_compute.remote(large_array))
results = ray.get(result_refs)
