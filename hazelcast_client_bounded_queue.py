import multiprocessing

from hazelcast import HazelcastClient

def put_data():
    client = HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members=["192.168.1.62:5701"]
        ,
        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )
    bounded_queue = client.get_queue("users").blocking()
    for i in range(100):
        bounded_queue.put(i)
        print("Put", i)
    print("Connected to cluster")


def read_data(id):
    client = HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members=["192.168.1.62:5701"]
        ,
        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )

    bounded_queue = client.get_queue("users").blocking()
    while bounded_queue.size() > 0:
        print("Client ", id, " read", bounded_queue.take())

    print("Connected to cluster")

if __name__ == "__main__":
    processes = []
    p = multiprocessing.Process(target=put_data)
    p.start()
    processes.append(p)
    for i in range(2):
        p = multiprocessing.Process(target=read_data, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print("Done!")