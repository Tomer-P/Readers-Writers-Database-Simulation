# Readers-Writers Database Simulation

A small educational Python project that simulates concurrent read/write access to a shared database-like file.

## Overview

The project demonstrates the core idea behind the classic **Readers-Writers synchronization problem**:

- Multiple readers may access the database concurrently.
- A writer must wait until active readers finish.
- Readers are blocked while a write operation is in progress.
- The simulation limits concurrent readers to 10.

The database is represented by a Python dictionary serialized to disk using `pickle`, while lightweight threads are used to simulate simultaneous clients.

## Project Structure

- `database_manager.py` — contains the database I/O layer, access manager, thread simulation, and interactive test menu.

## Main Components

### `DB_IO`
Handles reading from and writing to the serialized database file.

### `DB_Manager`
Tracks active readers and writer access, and decides whether read/write requests can be granted.

### Thread Simulation
Uses Python's `_thread` module and timed delays to simulate clients reading concurrently.

## Concepts Demonstrated

- Concurrency
- Threads
- Readers-Writers synchronization
- Shared-resource access control
- File I/O
- Serialization with `pickle`
- Basic object-oriented design

## Note

This is an educational simulation of synchronization logic rather than a production-safe concurrency implementation. The shared state is not protected by mutexes/locks, so race conditions are still possible in a real concurrent environment.

## Run

```bash
python database_manager.py
```

The program creates a local `grades` data file and presents an interactive menu for testing different read/write access scenarios.
