import subprocess
import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def run_cmd(*args):
    return subprocess.run(
        ["python3", "todo.py", *args],
        capture_output=True,
        text=True
    )


def write_tasks(data):
    TASKS_FILE.write_text(json.dumps(data, indent=2))


def read_tasks():
    return json.loads(TASKS_FILE.read_text())


# -------------------------
# TC-DONE-01
# BCC Base Case
# all = False, task_num = valid, tasks = not empty
# [a2, b2, c2]
# Mark valid task as done
# -------------------------
def test_done_base_case_valid_task_not_empty():
    write_tasks([
        {"name": "Task 1", "is_done": False}
    ])

    result = run_cmd("done", "1")
    tasks = read_tasks()

    assert result.returncode == 0
    assert tasks[0]["is_done"] is True


# -------------------------
# TC-DONE-02
# BCC Variation A
# all = True, task_num = valid/fixed, tasks = not empty
# [a1, b2, c2]
# Mark invalid task number
# -------------------------
def test_done_all_true_not_empty():
    write_tasks([
        {"name": "Task 1", "is_done": False}
    ])

    result = run_cmd("done", "999")
    tasks = read_tasks()

    assert result.returncode == 0
    assert tasks[0]["is_done"] is False


# -------------------------
# TC-DONE-03
# BCC Variation B
# all = False, task_num = invalid, tasks = not empty
# [a2, b3, c2]
# Mark all tasks as done
# -------------------------
def test_done_invalid_task_num_not_empty():
    write_tasks([
        {"name": "Task 1", "is_done": False},
        {"name": "Task 2", "is_done": False}
    ])

    result = run_cmd("done", "--all")
    tasks = read_tasks()

    assert result.returncode == 0
    assert all(task["is_done"] for task in tasks)


# -------------------------
# TC-DONE-04
# BCC Variation C
# all = False, task_num = valid, tasks = empty
# [a2, b2, c1]
# Done on empty task list
# -------------------------
def test_done_valid_task_empty_list():
    write_tasks([])

    result = run_cmd("done", "1")
    tasks = read_tasks()

    assert result.returncode == 0
    assert tasks == []