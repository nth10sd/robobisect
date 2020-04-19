# robobisect
Bisect repositories to find regression windows

## Assumptions:
* The WebKit/ repository is cloned into `~/WebKit/`.
* When bisection is in-progress, the `~/WebKit/` directory is left alone by the user/other programs that may interfere with the directory state of the repository.
