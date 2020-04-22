"""Class to create Gitrepo objects."""

import os
from pathlib import Path
import platform
import shutil
import subprocess

from git import Repo

from robobisect.compile_binary import Shell
from robobisect.util import git_helpers
from robobisect.util import utils


class Gitrepo:  # pylint: disable=missing-class-docstring,too-many-instance-attributes
    def __init__(self, remote_url, local_path):
        self.remote_url = remote_url
        self.local_path = local_path

        self.wk_cache = utils.mk_webkit_cache(Path.home())
        self.wk_rev_cache = None
        self.wk_rev_cache_lib = None
        self.wk_rev_cache_bin = None

        # Check the repository is working properly.
        self.repo = Repo(self.local_path)
        assert not self.repo.bare
        assert self.remote_url in self.repo.config_reader().get_value('remote "origin"', "url")
        assert not self.repo.is_dirty()

        self.rev = self.repo.git.rev_parse("--verify", "HEAD")

    def compile(self, rev):  # pylint: disable=missing-function-docstring,missing-return-doc,missing-return-type-doc
        wk_build_dir = Path.home() / "WebKit" / "WebKitBuild"

        # Set the rev in this Gitrepo object
        self.rev = rev

        self.wk_rev_cache = self.wk_cache / f"debug-{rev}"
        self.wk_rev_cache_lib = self.wk_rev_cache / "Debug" / "lib"
        self.wk_rev_cache_bin = self.wk_rev_cache / "Debug" / "bin" / "jsc"

        # First find the compiled versions in the cache directory
        if self.wk_rev_cache_bin.is_file():
            return self.wk_rev_cache_bin

        if wk_build_dir.is_dir():
            utils.RUN_LOG.info("Deleting %s!", wk_build_dir)
            shutil.rmtree(wk_build_dir)

        assert not self.repo.is_dirty()
        utils.RUN_LOG.info(self.repo.git.checkout([rev]))
        assert rev == self.repo.git.rev_parse("--verify", "HEAD")
        assert not self.repo.is_dirty()

        shell = Shell()
        try:
            shell_path = shell.compile()
        # Should propagate a different error from compile_binary, probably?
        except AssertionError:
            utils.RUN_LOG.info("The failing rev is: %s", rev)
            raise

        # Cache the compiled version
        if shell_path.is_file() and self.wk_cache.is_dir():
            wk_build_dir.rename(self.wk_rev_cache)

        return self.wk_rev_cache_bin

    def reset_bisect(self):  # pylint: disable=missing-function-docstring
        # If git wrapper commands fail, they throw GitCommandError.
        # Later: Capture this exception to always revert repo in case of failure
        assert not self.repo.is_dirty()
        utils.RUN_LOG.info(self.repo.git.bisect(["reset", "master"]))
        assert not self.repo.is_dirty()

    def set_bisect_result(self, rev, result):  # pylint: disable=missing-function-docstring,missing-return-doc
        # pylint: disable=missing-return-type-doc
        # Set the rev in this Gitrepo object
        self.rev = rev

        assert not self.repo.is_dirty()
        utils.RUN_LOG.info("Rev before bisect run is: %s", rev)

        bisect_result_msg = self.repo.git.bisect([result, rev])
        self.rev = self.repo.git.rev_parse("--verify", "HEAD")  # Update rev after each bisect run
        utils.RUN_LOG.info("Rev after bisect run is: %s", self.rev)
        utils.RUN_LOG.info(bisect_result_msg)
        assert not self.repo.is_dirty()

        return self.rev, bisect_result_msg

    def start_bisect(self):  # pylint: disable=missing-function-docstring
        assert not self.repo.is_dirty()
        utils.RUN_LOG.info(self.repo.git.switch(["master"]))
        assert not self.repo.is_dirty()
        utils.RUN_LOG.info(self.repo.git.bisect(["start", "--term-old=before", "--term-new=after"]))
        assert not self.repo.is_dirty()

        utils.RUN_LOG.info("Skipping changesets...")
        utils.RUN_LOG.info(self.repo.git.bisect(
            # Probably GCC 7-specific? (for Ubuntu 18.04)
            ["skip", git_helpers.broken_range(
                # SVN id 231170, approximately Apr 30 2018, SVN id 231223, approximately May 02 2018
                "b3c0f421637b2d8c89d85e236b760cf11c85f9e4", "2f9053265ff44547ba35184871fa9044e3993b7e",
            ).split()],
        ))
        utils.RUN_LOG.info(self.repo.git.bisect(
            ["skip", git_helpers.broken_range(
                # SVN id 238469, approximately Nov 24 2018, SVN id 238477, approximately Nov 25 2018
                "662fdd1c89968fde8d2ab41309c853b6771359d1", "a2794a6887461e04827d6d5c5373882ccd0707ca",
            ).split()],
        ))
        if platform.system() == "Linux":
            utils.RUN_LOG.info(self.repo.git.bisect(
                ["skip", git_helpers.broken_range(
                    # SVN id 251886, approximately Oct 31, 2019, SVN id 251912, approximately Nov 1 2019
                    "ae8c116a7bfea303684a7b7ca95a03559b4d5891", "cda9526a20e6d6456c56d0f67ad6566bad96c213",
                ).split()],
            ))
        utils.RUN_LOG.info("Finished skipping changesets...")

    def test(self, rev, runtime_params=None):  # pylint: disable=missing-function-docstring,missing-return-doc
        # pylint: disable=missing-return-type-doc
        if not self.wk_rev_cache_bin.is_file():
            raise OSError(f"Compiled shell at {rev} not found!")  # Comment out if testing for (compilation)
        # return "before" if self.wk_rev_cache_bin.is_file() else "after"  # Find regressor (compilation)
        # return "after" if self.wk_rev_cache_bin.is_file() else "before"  # Find fixed revision (compilation)

        if not runtime_params:
            runtime_params = ["-e", "42"]

        test_process = subprocess.run(
            [self.wk_rev_cache_bin] + runtime_params,
            check=False, cwd=self.wk_rev_cache_bin.parent,
            env=dict(os.environ, LD_LIBRARY_PATH=str(self.wk_rev_cache_lib)),
        )
        utils.RUN_LOG.info(test_process.returncode)

        return "after" if test_process.returncode else "before"  # Find regressor
        # return "before" if test_process.returncode else "after"  # Find fixed revision
