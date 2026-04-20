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


# -------------------------------------------------
# TC1
# delete --all
# Expected: All tasks deleted
# -------------------------------------------------
def test_delete_all_tasks():
    write_tasks([
        {"name": "Task 1", "is_done": False},
        {"name": "Task 2", "is_done": True}
    ])

    result = run_cmd("delete", "--all")
    tasks = read_tasks()

    assert result.returncode == 0
    assert tasks == []
    assert "all tasks deleted" in result.stdout.lower()


# -------------------------------------------------
# TC2
# delete 1
# Expected: Task deleted
# -------------------------------------------------
def test_delete_valid_task():
    write_tasks([
        {"name": "Task 1", "is_done": False},
        {"name": "Task 2", "is_done": False}
    ])

    result = run_cmd("delete", "1")
    tasks = read_tasks()

    assert result.returncode == 0
    assert len(tasks) == 1
    assert tasks[0]["name"] == "Task 2"
    assert "task deleted" in result.stdout.lower()


# -------------------------------------------------
# TC3
# delete 99
# Expected: Invalid task number
# -------------------------------------------------
def test_delete_invalid_task_number():
    write_tasks([
        {"name": "Task 1", "is_done": False}
    ])

    result = run_cmd("delete", "99")
    tasks = read_tasks()

    assert result.returncode == 0
    assert len(tasks) == 1
    assert tasks[0]["name"] == "Task 1"
    assert "invalid task number" in result.stdout.lower()


# -------------------------------------------------
# TC4
# delete
# Expected: No valid option
# -------------------------------------------------
def test_delete_no_valid_option():
    write_tasks([
        {"name": "Task 1", "is_done": False}
    ])

    result = run_cmd("delete")

    assert result.returncode == 0
    assert "no valid option" in result.stdout.lower()