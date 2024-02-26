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
        while True:
            value = my_map.get(1)
            updated_value = value + 1
            if my_map.replace_if_same(1, value, updated_value):
                break

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