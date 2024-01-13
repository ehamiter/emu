# Makefile for building the EMU executable

# Define the build command
build:
	pyinstaller --onefile emu.py

# Define a clean command to remove generated files
clean:
	rm -rf dist build __pycache__ *.spec

.PHONY: build clean
