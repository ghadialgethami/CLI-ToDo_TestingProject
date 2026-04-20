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
# ECC-01
# A4 (None), B2 (empty list)
# Missing task name
# -------------------------------------------------
def test_add_no_task_name_empty_list():
    write_tasks([])

    result = run_cmd("add")

    tasks = read_tasks()

    assert len(tasks) == 0
    assert "insert a task name" in result.stdout.lower()


# -------------------------------------------------
# ECC-02
# A3 (single word), B1 (not empty)
# -------------------------------------------------
def test_add_single_word_not_empty():
    write_tasks([
        {"name": "Old Task", "is_done": False}
    ])

    result = run_cmd("add", "Assignment1")

    tasks = read_tasks()

    assert result.returncode == 0
    assert tasks[-1]["name"] == "Assignment1"
    assert tasks[-1]["is_done"] is False


# -------------------------------------------------
# ECC-03
# A2 (multiple words with quotes), B1
# -------------------------------------------------
def test_add_multiword_with_quotes():
    write_tasks([
        {"name": "Old Task", "is_done": False}
    ])

    result = run_cmd("add", "Testing Project")

    tasks = read_tasks()

    assert result.returncode == 0
    assert tasks[-1]["name"] == "Testing Project"


# -------------------------------------------------
# ECC-04
# A1 (multiple words without quotes) → invalid input
# -------------------------------------------------
def test_add_multiple_words_without_quotes():
    write_tasks([
        {"name": "Old Task", "is_done": False}
    ])

    result = run_cmd("add", "Finish", "Assignment2")

    tasks = read_tasks()

    assert len(tasks) == 1  # no new task added
    assert "unexpected" in result.stderr.lower() or result.returncode != 0