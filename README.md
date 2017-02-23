# 1. internet2-multi-controller.py

使用mininet创建一个拓扑，并且各个节点与指定的不同控制器相连接。通过重写了OVSSwitch中的start()方法，从而使用指定的控制器连接各个交换机。

参考：

[mininet/examples/controllers.py](https://github.com/mininet/mininet/blob/master/examples/controllers.py)
