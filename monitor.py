#discovers active nodes and topics, identifies message types, displays publishers and subscribers
#and measures message activity across discovered topics.
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rosidl_runtime_py.utilities import get_message

class RosMonitor(Node):

    def __init__(self):
        super().__init__('ros_monitor')

        self.timer = self.create_timer(2.0, self.check_graph)
        self.topic_counts = {}
        self.topic_last_counts = {}
        self.topic_rates = {}
        self.topic_subscriptions = {}

    def topic_callback(self, msg, topic_name):
        self.topic_counts[topic_name] += 1
        
    def check_graph(self):
        nodes = self.get_node_names_and_namespaces()
        topics = self.get_topic_names_and_types()
        for topic_name, type_names in topics:
            if topic_name not in self.topic_subscriptions and type_names:
                try:
                    msg_type = get_message(type_names[0])

                    self.topic_counts[topic_name] = 0
                    self.topic_last_counts[topic_name] = 0
                    self.topic_rates[topic_name] = 0.0

                    callback = lambda msg, name=topic_name: self.topic_callback(msg, name)

                    self.topic_subscriptions[topic_name] = self.create_subscription(
                        msg_type,
                        topic_name,
                        callback,
                        10
                    )

                except Exception as exc:
                    self.get_logger().warning(
                        f"Cannot monitor {topic_name}: {exc}"
                    )
        for topic_name in self.topic_counts:
            current = self.topic_counts[topic_name]
            previous = self.topic_last_counts[topic_name]

            self.topic_rates[topic_name] = (current - previous) / 2.0
            self.topic_last_counts[topic_name] = current

        topic_names = {topic for topic, _ in topics}

        print("\033[2J\033[H", end="")

        print("================================")
        print("        ROS MONITOR")
        print("================================")
        print()

        # ----------------------------
        # Nodes
        # ----------------------------

        print(f"NODES ({len(nodes)})")
        print("--------------------------------")

        for name, namespace in nodes:
            if namespace == '/':
                print(f"  ● {name}")
            else:
                print(f"  ● {namespace}{name}")

        print()

        # ----------------------------
        # Topics
        # ----------------------------

        print(f"TOPICS ({len(topics)})")
        print("--------------------------------")

        for topic, types in topics:

            info = self.get_publishers_info_by_topic(topic)
            subscribers = self.get_subscriptions_info_by_topic(topic)

            print(f"  ● {topic}")
            print(f"       PUB {len(info)}   SUB {len(subscribers)}")
            if topic in self.topic_rates:
                rate = self.topic_rates[topic]

                print(f"       RATE {rate:.1f} Hz")

                if rate > 0:
                    print("       ● ACTIVE")
                else:
                    print("       ○ QUIET")
            for msg_type in types:
                print(f"       {msg_type}")

        # ----------------------------
        # Topic details
        # ----------------------------

        for topic, msg_types in topics:

            print()
            print("================================")
            print(f"  {topic} DETAILS")
            print("================================")

            publishers = self.get_publishers_info_by_topic(topic)
            subscribers = self.get_subscriptions_info_by_topic(topic)

            print()
            print("TYPE")
            print("--------------------------------")
            for msg_type in msg_types:
                print(f"  {msg_type}")

            print()
            print(f"PUBLISHERS ({len(publishers)})")
            print("--------------------------------")
            if publishers:
                for pub in publishers:
                    print(f"  ● {pub.node_name}")
            else:
                print("  —")

            print()
            print(f"SUBSCRIBERS ({len(subscribers)})")
            print("--------------------------------")
            if subscribers:
                for sub in subscribers:
                    print(f"  ● {sub.node_name}")
            else:
                print("  —")

        print("================================")


def main(args=None):
    rclpy.init(args=args)

    node = RosMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
