# robobisect
Bisect the WebKit Git repository to find regression windows. Currently focuses on JavaScriptCore (jsc) binaries.

## Why robobisect?
**NOTE: `robobisect` is still in alpha stage - do not use on a production machine.**

Depending on the computer `robobisect` is run on, with an Intel Core i7-9700K (8C/8T), a NVMe SSD and 32GB RAM on Ubuntu 18.04, each changeset compiles in less than 4 minutes, and due to binary search, a bisect result is obtained within about 15 compiles (assuming the starting and ending working states are known), thus only takes approximately **an hour** to run fully. If you have a slower computer (e.g. with a spinning HDD), your compile times are expected to be slower. If you have `ccache`, and if your changeset has already been compiled before and is in the cache, your compile times should speed up considerably for that changeset.

As of April 2020, `robobisect` is able to test as far back as May 2017, or about 3 years worth of history.

Having an exact regressing changeset in a bug report is extremely useful information for developers, as it can show whether it is the cause of the bug or one that caused the latent bug to show up.

`robobisect` can test when builds started to fail compilation, and verify when testcases were fixed by which revision. It can also be used to find when a bug is fixed, or stopped reproducing, or when the stdout message changed.

## How do I use robobisect?
```rm -rf ~/WebKit/WebKitBuild/ && time { date && python3.8 -m robobisect 2>&1 | tee ~/rb_log.txt ; date ; }```

Note: argparse is on the to-do list. Some functions not working well yet - one has to change `robobisect` itself to test various stuff.

## Does this work on macOS / Windows 10?
`robobisect` has been tested to run on Ubuntu 18.04. I do not yet have a recent macOS machine powerful enough for sane compilation times, ideas welcome. Windows 10 support will fall behind Ubuntu Linux and macOS for now. Other flavours of Linux probably are not yet a priority anytime soon.

## Why not bisect-builds (from the WebKit repository)?
WebKit already has the [bisect-builds](https://github.com/WebKit/webkit/blob/master/Tools/Scripts/bisect-builds) script, but this uses downloaded pre-compiled builds. This method is faster than `robobisect`, which uses source-compiled builds, but whether `bisect-builds` gives a single regressing changeset will depend on how often the pre-compiled builds were created. If they are per-push, `bisect-builds` will give a single regressing changeset, but if they are per-day, `bisect-builds` will give a range of changesets.

`robobisect` usually provides a tighter bisect unless it falls within a range of non-compilable changesets. Moreover, `robobisect` will allow supporting different configurations which are not part of the pre-compiled builds. For bugs which occur only on specific systems (and not with pre-compiled builds), provided the binary can be compiled and the dev toolchain installed, `robobisect` may be able to come up with a regressing changeset.

## How does this work?
`robobisect` compiles into a cache folder, which is then used to test against a given testcase. It acts as a higher-level interface on top of `git bisect`.

## Will this support the WebKit browser itself?
Possibly, at some point. Previous incantations of `autobisectjs` used to support the Firefox browser instead of just SpiderMonkey.

## Will this support other browsers?
Gecko has [autobisect](https://github.com/MozillaSecurity/autobisect/) for Firefox and [autobisectjs](https://github.com/MozillaSecurity/funfuzz/blob/master/src/funfuzz/autobisectjs/autobisectjs.py) for SpiderMonkey, while Chrome has [bisect-builds.py](https://www.chromium.org/developers/bisect-builds-py) and [Chrome Bisect](https://github.com/jay0lee/chrome-bisect). Edge Chromium only publishes source code dumps.

At some point in the distant future, `robobisect` may be adapted to work with [Gecko-dev](https://github.com/mozilla/gecko-dev).

## Can this be in a Docker/&lt;favourite container&gt; format?
Not sure about the benefits of the container format for now.

## TODO:
* argparse
* Be able to specify desired repo start and end-points. Currently defaults to earliest known working revision, and master.
* Improve the cache - it seems like only the `jsc` binary and the files in `Debug/lib` are needed
* Add test for +2/-2 from ([WebKit bug 187947](https://bugs.webkit.org/show_bug.cgi?id=187947)) - when testcase is fixed
* Add test for +2/-2 from ([WebKit bug 203406](https://bugs.webkit.org/show_bug.cgi?id=203406)) - when testcase started failing
* Consider adding a lock dir (via fasteners?) when robobisect is running.
* CI support (via Travis?)
* Code coverage (via codecov.io?)

## Assumptions:
* The WebKit/ repository is cloned into `~/WebKit/`.
* When bisection is in-progress, the `~/WebKit/` directory is left alone by the user/other programs that may interfere with the directory state of the repository.
