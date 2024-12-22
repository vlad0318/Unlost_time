# Unlost_time
Time management app

# Memory module

How to use:
    First import the memory module
    Next set a variable equal to memory.memory()
    From there you can use the features using this syntax var_name.feature()
        This initates a dictionary for the features to be added to

    Features:
        var_name.add_task("name of task", "time", "importance", "location")
            This feature lets you add tasks to the memory file by passing the info of the task
        
        var_name.remove_task("task name")
            this feature lets you remove a task by passing the task name

        var_name.read_json()
            This feature allows you to read the json file and output a dictionary to a var if assinged to one

        var_name.write()
            This feature allows you to write all the tasks that you added to the memory dictionary to the file
