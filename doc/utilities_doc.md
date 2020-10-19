# Utilities (lattice2d.utilities)

This package contains many different useful classes and functions, which will be grouped and described below.

## Bounds (lattice2d.utilities.bounds)
These functions determine whether a point is in a shape.

- within_circle_bounds: determines whether a point is within a circle
- within_rect_bounds: determines whether a point is within a rectangle
- within_square_bounds: determines whether a point is within a square

## Log (lattice2d.utilities.log)
This is a useful logger with color coding and a customizable log level.  Log flags and their corresponding colors can be set in the configuration, and then using the log function is as easy as passing the string you want to print and the flag to it.  If the flag is included in the configuration, it will be printed.

## GetPageInfo (lattice2d.utilities.get_page_info)
This package contains a single function `get_page_info` that returns the indices of the elements and indications whether paging forward or backward is possible, given the current page, the size of each page, and the total count of elements.

Example: `[3, 5, False, True] = get_page_info(1, 3, 6)`

## ThreadedQueue (lattice2d.utilities.threaded_queue)
This package contains a deque that requires obtaining a lock to read from and write to.  This class also provides deque functionality used by the classes in this repository (`has_elements`, `popleft`, and `append`).

## ThreadedSync (lattice2d.utilities.threaded_sync)
This package contains a means to make all clients wait on other clients at a particular point.  This class contains a count set on construction and protected by a lock on reads and writes, and only once the `count` method is called the number of times specified will the `done` method return true.
