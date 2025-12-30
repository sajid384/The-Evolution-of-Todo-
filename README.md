# Persistent Todo Console App

A command-line interface (CLI) application for managing todo tasks with JSON persistence and interactive shell, built with Python 3.13+.

## Features

- Add tasks with title and description
- View all tasks with ID and status
- Update task title and description
- Delete tasks by ID
- Mark tasks as complete/incomplete
- Toggle task completion status
- JSON file persistence (default: ~/.todo/todos.json)
- Interactive shell mode for continuous task management
- Tab completion and command history in shell mode
- Custom data file location support

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Setup Instructions

### 1. Install UV

If you don't have UV installed, you can install it using pip:

```bash
pip install uv
```

Or follow the official installation instructions at [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

### 2. Clone or Download the Project

```bash
git clone <repository-url>
cd todo-inmemory-cli
```

### 3. Create Virtual Environment and Install Dependencies

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 4. Verify Installation

```bash
todo --help
```

## Usage

### Add a Task

```bash
todo add "Task Title" "Task Description"
# Or using alias
todo a "Task Title" "Task Description"
```

### List All Tasks

```bash
todo list
# Or using aliases
todo l
todo ls
```

### Update a Task

```bash
todo update <task_id> "New Title" "New Description"
# Or update only title
todo update <task_id> "New Title"
# Or update only description
todo update <task_id> "" "New Description"
# Using alias
todo u <task_id> "New Title" "New Description"
```

### Delete a Task

```bash
todo delete <task_id>
# Using alias
todo d <task_id>
```

### Mark Task as Complete

```bash
todo complete <task_id>
# Using alias
todo c <task_id>
```

### Mark Task as Incomplete

```bash
todo incomplete <task_id>
# Using alias
todo i <task_id>
```

### Toggle Task Status

```bash
todo toggle <task_id>
# Using alias
todo t <task_id>
```

### Get Help

```bash
todo help
todo --help
todo -h
```

### Start Interactive Shell

```bash
todo shell
# Or using alias
todo sh
```

In shell mode, you can run commands without the 'todo' prefix:
```bash
> add "Buy groceries" "Milk, bread, eggs"
> list
> complete 1
> status
> stats
> exit
```

### Custom Data File Location

```bash
todo --data-file /path/to/custom/todos.json list
# Or using environment variable
TODO_FILE=/path/to/custom/todos.json todo list
```

## Examples

```bash
# Add a task
todo add "Buy groceries" "Milk, bread, eggs"

# List all tasks
todo list

# Update a task
todo update 1 "Updated task title" "Updated description"

# Mark a task as complete
todo complete 1

# Toggle a task status
todo toggle 2

# Delete a task
todo delete 3

# Start interactive shell
todo shell

# Use custom data file
todo --data-file ./my-todos.json list

# Set environment variable for data file
TODO_FILE=./my-todos.json todo add "Task with custom file"
```

## Architecture

The application follows clean architecture principles:

- **Core**: Contains domain entities and business rules
- **Data**: Handles in-memory storage and retrieval
- **Services**: Contains application-specific business logic
- **CLI**: Handles command-line interface interactions
- **App**: Orchestrates the entire application flow
- **Utils**: Contains reusable utility functions

## Constraints

- Data is stored in JSON file by default (persistence across sessions)
- Optional in-memory mode available
- No external dependencies beyond Python standard library
- Console-based interface only

## License

This project is licensed under the MIT License.