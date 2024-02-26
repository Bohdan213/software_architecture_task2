import multiprocessing

from hazelcast import HazelcastClient
import time

def put_map():
    client = HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members=["192.168.1.62:5701",
                         "192.168.1.62:5702",
                         "192.168.1.62:5703", ]
        ,
        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )

    print("Connected to cluster")

    my_map = client.get_map("users").blocking()
    for i in range(10000):
        my_map.lock(1)
        try:
            value = my_map.get(1)
            value += 1
            my_map.put(1, value)
        finally:
            my_map.unlock(1)

    client.shutdown()


if __name__ == "__main__":
    start = time.time()
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=put_map)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print("Done!")
    end = time.time()
    print("Time elapsed: ", end - start)
