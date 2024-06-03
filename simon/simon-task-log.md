# Work log (Simon Tran)

## Completed Tasks

- Installed Qhull and setup personal local repository
- Helped Eden setup and install Qhull, Git and a simple text editor (previously she was usually Windows Notepad).
- Refactored code
    - Added type hints for clarity, `black` and `isort` for import formatting for consistent formatting, and `flake8` for linting
    - Added crucial `plt.show()` for `matplotlib` planar graph
    - Modified STDOUT messages
    - Segmented code into distinct functions and different files
    - Simplified code
    - Modified argument parsing to use Python's standard library `argparse`. This fixes issues program crashes or unexpected behavior like when a user mistypes options, or when a user inputs a negative number of points. Also, the default positional arguments are now properly set (e.g. previously, the default of 10 points didn't work properly)
    - Modify code such that
- Wrote a `README.md` with a description of the project, and an installation and usage guide
- Complete edge to face map, ensuring the outer face edges are ordered in a counter-clockwise manner
- Refactored remaining code for graph generation and plotting
- Created an adjacency list
- Refactored code into more independent functions
- Simplified graph plotting
- label the vertices and the faces

## TO DO