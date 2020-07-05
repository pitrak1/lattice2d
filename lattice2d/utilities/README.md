# Utilities (lattice2d.utilities)

This package contains many different useful classes and functions, which will be grouped and described below.

## Bounds (lattice2d.utilities.bounds)
These functions determine whether a point is in a shape.

- within_circle_bounds: determines whether a point is within a circle
- within_rect_bounds: determines whether a point is within a rectangle
- within_square_bounds: determines whether a point is within a square

## Log (lattice2d.utilities.log)
This is a useful logger with color coding, indentation, and a customizable log level.

The log levels are as follows:
- LOG_LEVEL_HIGH
- LOG_LEVEL_MEDIUM
- LOG_LEVEL_LOW
- LOG_LEVEL_INTERNAL_HIGH
- LOG_LEVEL_INTERNAL_LOW

The level can be configured (see the Configuration section for details), and setting a level will print messages on that level and above.  For instance, setting the level to `LOG_LEVEL_LOW` will read all messages logged at that level as well as `LOG_LEVEL_MEDIUM` and `LOG_LEVEL_HIGH`.  Log level for a particular message needs to be set each time a message is sent (for example: `log('some message', LOG_LEVEL_MEDIUM))`)

## GetPageInfo (lattice2d.utilities.get_page_info)
This package contains a single function `get_page_info` that returns the indices of the elements and indications whether paging forward or backward is possible, given the current page, the size of each page, and the total count of elements.

Example: `[3, 5, False, True] = get_page_info(1, 3, 6)`

## ThreadedQueue (lattice2d.utilities.threaded_queue)
This package contains a deque that requires obtaining a lock to read from and write to.  This class also provides deque functionality used by the classes in this repository (`has_elements`, `popleft`, and `append`).

## ThreadedSync (lattice2d.utilities.threaded_sync)
This package contains a means to make all clients wait on other clients at a particular point.  This class contains a count set on contruction and protected by a lock on reads and writes, and only once the `count` method is called the number of times specified will the `done` method return true.