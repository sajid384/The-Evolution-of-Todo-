# Phase II: Persistent Todo CLI with Interactive Shell - Implementation Plan

## Overview

This implementation plan outlines the Agentic Dev Stack approach for implementing Phase II of the Todo CLI application, which adds JSON persistence and interactive shell mode while maintaining backward compatibility with existing functionality.

## Architecture Changes

### 1. Data Layer Modifications
- **Repository Pattern Extension**: Extend the existing in-memory repository to support file-based persistence
- **New File-based Repository**: Create `FileTaskRepository` that implements the same interface as the in-memory repository
- **Repository Factory**: Implement a factory pattern to choose between in-memory and file-based repositories based on configuration

### 2. Service Layer Updates
- **Task Service Enhancement**: Update `TaskService` to work with the new repository implementation
- **Configuration Service**: Add a new service to handle file location configuration and environment variables

### 3. CLI Layer Extensions
- **New Shell Module**: Create a dedicated module for interactive shell functionality
- **Command Parser Enhancement**: Extend parser to recognize the new `shell` command
- **Help System Update**: Include documentation for new shell features

### 4. Application Layer Modifications
- **Main Application**: Update to support shell mode entry point
- **Dependency Injection**: Configure new services and repositories based on runtime options

## New Modules to be Created

### 1. `src/data/file_repository.py`
- Implements `FileTaskRepository` class
- Handles JSON file I/O operations
- Manages file locking and error handling
- Provides methods for loading/saving tasks to/from JSON

### 2. `src/data/config.py`
- Configuration management for file locations
- Environment variable handling
- Default path resolution logic
- File permission validation

### 3. `src/shell/` directory
- **`shell_manager.py`**: Main shell orchestration class
- **`shell_commands.py`**: Command handlers for shell-specific functionality
- **`shell_completer.py`**: Tab completion logic
- **`shell_history.py`**: Command history management

### 4. `src/services/config_service.py`
- Centralized configuration service
- Handles file location resolution
- Manages default paths and custom overrides

### 5. `src/utils/file_utils.py`
- File system utilities for JSON operations
- File locking mechanisms
- Directory creation utilities
- Error handling for file operations

## Data Flow

### 1. Application Startup Flow
```
main() → parse_args() → config_service.resolve_file_path() → file_repository.load_tasks() → task_service.initialize()
```

### 2. Command Execution Flow (Non-Shell)
```
cli_parser.parse() → task_service.execute_command() → file_repository.save_tasks() → output_formatter.format()
```

### 3. Shell Mode Flow
```
shell_manager.start() → shell_completer.setup() → loop:
  - prompt() → parse_input() → dispatch_command() → execute_command() → save_if_modified() → continue_or_exit()
```

### 4. File Persistence Flow
```
load_tasks_from_file() → validate_json() → create_task_objects() → store_in_memory()
```
```
command_executed() → update_in_memory() → serialize_to_json() → write_to_file() → handle_errors()
```

## Execution Order

### Phase 1: Foundation (Week 1)
1. **Create configuration module** (`src/data/config.py`)
   - Implement file path resolution logic
   - Add environment variable handling
   - Create default path determination

2. **Create file utilities** (`src/utils/file_utils.py`)
   - Implement JSON read/write functions
   - Add file locking mechanisms
   - Create error handling utilities

3. **Create file-based repository** (`src/data/file_repository.py`)
   - Implement `FileTaskRepository` class
   - Add file I/O operations
   - Include error handling and validation

### Phase 2: Core Persistence (Week 1-2)
4. **Update service layer** (`src/services/config_service.py`)
   - Create configuration service
   - Implement repository factory pattern
   - Add backward compatibility layer

5. **Integrate persistence into main application**
   - Update `src/app/main.py` to use file repository
   - Add command-line flag support for custom file location
   - Maintain in-memory fallback for backward compatibility

6. **Update existing tests** to work with new persistence layer
   - Modify test fixtures
   - Add file-based test scenarios

### Phase 3: Shell Implementation (Week 2-3)
7. **Create shell infrastructure** (`src/shell/`)
   - Implement `ShellManager` class
   - Add basic command loop
   - Create custom prompt

8. **Implement shell commands**
   - Create `ShellCommands` class
   - Map existing CLI commands to shell equivalents
   - Add special shell commands (`help`, `clear`, `status`, `stats`)

9. **Add shell features**
   - Implement tab completion (`shell_completer.py`)
   - Add command history (`shell_history.py`)
   - Create argument parsing for shell context

### Phase 4: Integration and Testing (Week 3-4)
10. **Integrate shell with main application**
    - Add `shell` command to CLI parser
    - Connect shell to task service
    - Implement graceful exit and data saving

11. **Update help system**
    - Add shell-specific help documentation
    - Include examples for shell usage
    - Update command reference

12. **Comprehensive testing**
    - Test file persistence scenarios
    - Test shell functionality
    - Verify backward compatibility
    - Performance testing for file operations

### Phase 5: Error Handling and Polish (Week 4)
13. **Implement comprehensive error handling**
    - File system errors
    - Data corruption recovery
    - Shell input validation

14. **Add security measures**
    - File permission validation
    - Path traversal protection
    - Secure file operations

15. **Performance optimization**
    - Caching for frequent file operations
    - Efficient serialization/deserialization
    - Optimize shell response time

## Dependencies and Integration Points

### 1. Core Dependencies
- Existing `Task` entity from `src/core/task.py`
- `TaskService` from `src/services/task_service.py`
- `OutputFormatter` from `src/cli/output_formatter.py`

### 2. External Dependencies
- Python's `cmd` module for shell implementation
- `json` module for file operations
- `os`, `pathlib` for file system operations
- `threading` for file locking if needed

### 3. Testing Considerations
- Mock file system operations for unit tests
- Temporary file handling for integration tests
- Isolated test environments for file persistence

## Risk Mitigation

### 1. Data Corruption Risk
- Implement atomic file writes
- Create backup mechanisms
- Add data validation on load

### 2. Performance Impact
- Implement caching to reduce file I/O
- Optimize JSON serialization
- Add lazy loading where appropriate

### 3. Backward Compatibility
- Maintain all existing interfaces
- Provide fallback mechanisms
- Thorough regression testing

## Success Metrics

### 1. Functional Metrics
- All existing CLI commands work without changes
- File persistence works correctly
- Shell mode functions as specified
- Error handling covers all scenarios

### 2. Performance Metrics
- File loading under 2 seconds for 10,000 tasks
- File saving under 1 second for 10,000 tasks
- Shell response time under 100ms

### 3. Quality Metrics
- All acceptance criteria met
- Code coverage maintained or improved
- No regressions in existing functionality
- Comprehensive test coverage for new features