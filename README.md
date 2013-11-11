# Log Utilities

This project contains modules/classes/functions that extend the built-in
logging module. 

## log_rotate.py

This module contains the FilenamePatternFileHandler that can be used to automatically
rotate logging files at initialization based on a defined filename pattern
and the current date. This subclass of ``logging.FileHandler`` provides a very
simple mechanism that serves well for quick executing scripts that are run
many times over a period of time. 

### Reasons for this FileHandler?

I could not get the built-in ``logging.handlers.TimedRotatingFileHandler`` to suit
my needs as it only works for long running applications, like background processes
and servers, when the app is restarted, the rotating is reset. I needed my loggers
to handle rotating files (at the start of script execution) without having to
know anything about the file(s) it logs to. This subclass of FileHandler does
just that.


### Examples:

Let's say you had a script that runs every hour, does some task for a few minutes,
and logs the actions to a file. Now let's say that instead of writing to the same
log file each run, you want it to rotate every day, to make the logs more condensed,
and organized. To do that you can use ``FilenamePatternFileHandler``:

    import logging
    import log_rotate
    logger = logging.getLogger('example')

    handler = log_rotate.FilenamePatternHandler(
    	"example_log-{date}.log",
    	interval="D"
    )
	logger.addHandler(handler)


The first argument to ``FilenamePatternFileHandler`` is the *pattern*. The
*pattern* is a string that you define that will help determine what the
filename is. The key thing here is to include the *{date}* string format
keyword to the pattern. This tells ``FilenamePatternFileHandler`` where
to insert the current date in the filename, as it handles how the date
is represented in the filename. Based on *interval* you specify, it determines
how the date looks which, in turn, is how the rotation is indirectly handled.

As of this writing, the ``FilenamePatternFileHandler`` has support for the
following intervals:

* **S** - *rotate per second*
* **MIN** - *rotate each minute*
* **H** - *rotate each hour*
* **D** - *rotate daily*
* **M** - *rotate monthly*

## TODO

* Provide support for date formatting based on locale.
* Add more intervals (Yearly, bi-weekly, bi-hourly...?)
