# kboard

Console-based Kanban task manager created in Python.

Create and manage tasks visually in your terminal using handy commands.

## Features

- CLI based Kanban board.
- Easy setup.
- Simple commands.
- Structured database file.

## Installation

Install using pip running the following command in the terminal:

## Usage

If you installed the library, you can use the CLI as a system command:

```sh
kb COMMAND [ARGS] ...
```

### Examples

Here are some examples of the commands available:

```sh
# List the existing boards.
kb board ls

# Create a new board.
kb board add "Board name"

# Add a task to the backlog.
kb task add "Task title"

# Add a task to a board with high priority.
kb task add --board 1 --priority 3 "Important task"

# Move a task
kb task mv 2
```

## Contributing

Thank you for considering contributing to my project! Any pull requests are
welcome and greatly appreciated. If you encounter any issues while using
the project, please feel free to post them on the issue tracker.

To contribute to the project, please follow these steps:

1. Fork the repository.
2. Add a new feature or bug fix.
3. Commit them using descriptive messages, using
   [conventional commits](https://www.conventionalcommits.org/) is recommended.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for more details.
