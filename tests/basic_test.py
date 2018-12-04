import CostumePy

test1 = CostumePy.new_node("test1")

def callback_function(msg):
    print("ping %r" % msg)

test1.listen_to("ping", callback_function)


for i in range(10):
    new_node = CostumePy.new_node("%s_test" % i)
    new_node.broadcast_message(CostumePy.message("ping"))