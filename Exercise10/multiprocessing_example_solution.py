from multiprocessing import Process, Queue
import threading
import time

def find_primes(n, results=None, idx=None):
    """
    Find the number of prime numbers less than or equal to n.
    
    Args:
        n (int): The upper limit for finding prime numbers.
        results (Queue/List, optional): A queue or a List to store the result. Defaults to None.
        idx (int, optional): The index to store the result in the queue. Defaults to None.
    
    Returns:
        int: The number of prime numbers less than or equal to n.
    """
    prime = [True for _ in range(n+1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1
    n_primes = sum(prime) - 2

    if results is not None and idx is not None:
        results[idx] = [n, n_primes]
    elif results is not None:
        results.put([n, n_primes])
    else:
        return n_primes
    

#NUMBERS = [20_000_000]
NUMBERS = [20_000_000, 20_000_000, 20_000_000, 20_000_000]

##################################
# Single thread
##################################
if __name__ == "__main__":

    start = time.time()

    results = []
    for n in NUMBERS:
        results.append([n, find_primes(n)])

    end = time.time()

    print("SINGLE THREAD Results:")
    print(f"Time taken: {end - start} seconds")
    for n, n_primes in results:
        print(f"{n}: {n_primes} primes")


##################################
# Multiprocessing
##################################
if __name__ == "__main__":

    start = time.time()

    queue = Queue()
    jobs = []
    for n in NUMBERS:
        proc = Process(target=find_primes, args=(n, queue))
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
    for n, n_primes in results:
        print(f"{n}: {n_primes} primes")


##################################
# Multithreading
##################################
if __name__ == "__main__":
    start = time.time()

    results = [None] * len(NUMBERS)

    jobs = []
    for idx, n in enumerate(NUMBERS):
        thread = threading.Thread(target=find_primes, args=(n, results, idx))
        jobs.append(thread)
        thread.start()

    for thread in jobs:
        thread.join()

    end = time.time()

    print("MULTITHREADING Results:")
    print(f"Time taken: {end - start} seconds")
    for res in results:
        n, n_primes = res
        print(f"{n}: {n_primes} primes")