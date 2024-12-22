import memory

i=memory.memory()

i.add_task("code", "now", "low", "unspecified")
i.add_task("code", "then", "high", "unspecified")
i.add_task("work", "now", "high", "unspecified")

i.write()

i.read_json()


i.remove_task("work")

i.write()
