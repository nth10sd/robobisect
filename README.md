# robobisect
Bisect the WebKit Git repository to find regression windows. Currently focuses on JavaScriptCore (jsc) binaries.

## Why robobisect?
Depending on the computer `robobisect` is run on, with an Intel Core i7-9700K (8C/8T), a NVMe SSD and 32GB RAM on Ubuntu 18.04, each changeset compiles in less than 4 minutes, and due to binary search, a bisect result is obtained within about 15 compiles (assuming the starting and ending working states are known), thus only takes approximately **an hour** to run fully. If you have a slower computer (e.g. with a spinning HDD), your compile times are expected to be slower. If you have `ccache`, and if your changeset has already been compiled before and is in the cache, your compile times should speed up considerably for that changeset.

As of April 2020, `robobisect` is able to test as far back as May 2017, or about 3 years worth of history.

Having an exact regressing changeset in a bug report is extremely useful information for developers, as it can show whether it is the cause of the bug or one that caused the latent bug to show up.

## How do I use robobisect?
TBD

## Why not bisect-builds (from the WebKit repository)?
WebKit already has the [bisect-builds](https://github.com/WebKit/webkit/blob/master/Tools/Scripts/bisect-builds) script, but this uses downloaded pre-compiled builds. This method is faster than `robobisect`, which uses source-compiled builds, but whether `bisect-builds` gives a single regressing changeset will depend on how often the pre-compiled builds were created. If they are per-push, `bisect-builds` will give a single regressing changeset, but if they are per-day, `bisect-builds` will give a range of changesets.

`robobisect` usually provides a tighter bisect unless it falls within a range of non-compilable changesets. Moreover, `robobisect` will allow supporting different configurations which are not part of the pre-compiled builds. For bugs which occur only on specific systems (and not with pre-compiled builds), provided the binary can be compiled and the dev toolchain installed, `robobisect` may be able to come up with a regressing changeset.

## What are some other uses of robobisect?
`robobisect` may be used to find when a bug is fixed, or stopped reproducing, or when the stdout changed, as such differences do not matter to `git bisect`. It can also be used to find out when changesets stopped compiling.

## How does this work?
`robobisect` compiles into a binary into the `WebKitBuild/` directory, which is then used to test against a given testcase. The directory is then blown away as other revisions are tested. At some point, it should maybe be able to (1) compile into a different directory directly, or (2) at least move the compiled directory away post-compilation as a form of cache, then move it back in when testing.

## Will this support the WebKit browser itself?
Possibly, at some point. Previous incantations of `autobisectjs` used to support the Firefox browser instead of just SpiderMonkey.

## Will this support other browsers?
Gecko has [autobisect](https://github.com/MozillaSecurity/autobisect/) for Firefox and [autobisectjs](https://github.com/MozillaSecurity/funfuzz/blob/master/src/funfuzz/autobisectjs/autobisectjs.py) for SpiderMonkey, while Chrome has [bisect-builds.py](https://www.chromium.org/developers/bisect-builds-py) and [Chrome Bisect](https://github.com/jay0lee/chrome-bisect). Edge Chromium only publishes source code dumps.

## Can this be in a Docker/&lt;favourite container&gt; format?
Not sure about the benefits of the container format for now.

## TODO:
* Be able to specify desired repo start and end-points. Currently defaults to earliest known working revision, and master.
* In cache, jsc-dbg-REVHASH if clobber off
* Support known broken ranges
* Add test for +2/-2 from WebKit git rev 18cd04a58b7 ([WebKit bug 187947](https://bugs.webkit.org/show_bug.cgi?id=187947))
* Consider adding a lock dir (via fasteners?) when robobisect is running.

## Assumptions:
* The WebKit/ repository is cloned into `~/WebKit/`.
* When bisection is in-progress, the `~/WebKit/` directory is left alone by the user/other programs that may interfere with the directory state of the repository.
