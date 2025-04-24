from multiprocessing import Process, Queue
import time

# Function to approximate Pi
def approximate_pi(n, results=None, idx=None):
    pi_2 = 1
    nom, den = 2.0, 1.0
    for i in range(n):
        pi_2 *= nom / den
        if i % 2:
            nom += 2
        else:
            den += 2
    approx_pi = 2 * pi_2

    
    if results is not None and idx is not None:
        results[idx] = [n, approx_pi]
    elif results is not None:
        results.put([n, approx_pi])
    else:
        return approx_pi

# List of N values to process
nums = [1_822_725, 22_059_421, 32_374_695, 88_754_320, 97_162_66, 200_745_654]

# Function to parallelize the computation
if __name__ == "__main__":

    start = time.time()

    queue = Queue()
    jobs = []
    for n in nums:
        proc = Process(target=approximate_pi, args=(n, queue))
        jobs.append(proc)
        proc.start()

    for proc in jobs:
        proc.join()

    results = []
    while not queue.empty():
        results.append(queue.get())

    end = time.time()

    print("MULTIPROCESSING Results:")
    print(f"Time taken: {end - start} seconds")
    for result in results:
        print(f"N =: Approximation of Pi = {result}")
    print(results)