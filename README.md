# 1. internet2-multi-controller.py

使用mininet创建一个拓扑，并且各个节点与指定的不同控制器相连接。通过重写了OVSSwitch中的start()方法，从而使用指定的控制器连接各个交换机。

参考：

[mininet/examples/controllers.py](https://github.com/mininet/mininet/blob/master/examples/controllers.py)

# 2. linear-multi-controller.py

使用mininet创建一个POF linear拓扑，与创建OVS Linear拓扑不同的是需要重写Linear
Topo类，从而在创建交换机时指定ListenPort: switch = self.addSwitch('s%s' % i, listenPort = 6633 + i)，否则创建拓扑会失败。