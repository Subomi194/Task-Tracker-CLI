import json
from datetime import datetime
import sys

def load_tasks():
    try:
        with open('tasks_data.json', 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError ):
        data = []
    return data
    
def save_tasks(data):
    with open('tasks_data.json', 'w') as f:
        json.dump(data, f, indent=4)


def add_task(description):
    data = load_tasks()

    if data:
        next_id = max(task['id'] for task in data) + 1
    else:
        next_id = 1
    
    task = {
        'id': next_id,
        'description': description,
        'status': 'todo',
        'createdAt':  datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updatedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data.append(task)

    save_tasks(data)
    print(f'Task added successfully (ID:{next_id})')

def update_task(id, new_description):
    data = load_tasks()

    for task in data:
        if task['id'] == id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not any(task['id'] == id for task in data):
        print(f'Task with (ID:{id}) not found')
        return
    
    save_tasks(data)
    print(f'Task (ID:{id}) updated successfully ')

def delete_task(id):
    data = load_tasks()

    for task in data:
        if task['id'] == id:
            data.remove(task)
            break

    if not any(task['id'] == id for task in data):
        print(f'Task with (ID:{id}) not found')
        return

    save_tasks(data)
    print(f'Task (ID:{id}) deleted successfully ')

def update_status(id, new_status):
    data = load_tasks()

    for task in data:
        if task['id'] == id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_tasks(data) 
            print(f'Task marked as {new_status} successfully') 
            return

    print(f'Task with (ID:{id}) not found') 
        
def list_all_tasks():
    data = load_tasks()

    for task in data:
        print(f"[{task['id']}] {task['description']} - {task['status']} ")

def list_by_status(status):
    data = load_tasks()

    for task in data:
        if task['status'] == status:
            print(f"[{task['id']}] {task['description']} - {task['status']} ")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a command")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task description")
            sys.exit(1)

        description = sys.argv[2]
        add_task(description)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Please provide a task ID and a new desceiption")
            sys.exit(1)

        id = int(sys.argv[2])
        new_description = sys.argv[3]
        update_task(id, new_description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide a task ID")
            sys.exit(1)

        id = int(sys.argv[2])
        delete_task(id)
    
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Please provide a task ID")
            sys.exit(1)

        id = int(sys.argv[2])
        update_status(id, "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Please provide a task ID")
            sys.exit(1)

        id = int(sys.argv[2])
        update_status(id, "done")

    elif command == "list":
        if len(sys.argv) == 2:
            list_all_tasks()
        elif len(sys.argv) == 3:
            status = sys.argv[2]
            list_by_status(status)
        else:
            print(f'Invalid list command')

    else:
        print("Unknown command")
        
    
