from hazelcast import HazelcastClient


client = HazelcastClient(
    cluster_name = "hazelcast-cluster",
    cluster_members = ["192.168.1.62:5701",
                       "192.168.1.62:5702",
                       "192.168.1.62:5703",]
    ,
    lifecycle_listeners=[
        lambda state: print("Lifecycle event >>>", state),
    ]
)
print("Connected to cluster")

my_map = client.get_map("users").blocking()
# for i in range(1000):
#     my_map.put(i, i)
my_map.put(1, 0)
client.shutdown()
