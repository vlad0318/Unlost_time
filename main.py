import memory

i=memory.memory()

i.add_task("code", "now", "low", "unspecified")
i.add_task("code", "then", "high", "unspecified")
i.add_task("work", "now", "high", "unspecified")

i.write()

x=i.read_json()

print(x)

i.remove_task("work")

i.write()
