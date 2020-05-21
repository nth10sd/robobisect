"""Start bisection here."""

from pathlib import Path

from robobisect.git_repo import Gitrepo


def main():  # pylint: disable=missing-raises-doc
    """Main function to start bisection."""

    testcase = None
    # testcase = Path.home() / "robobisect" / "tests" / "JSTests" / "stress" / "regress-187947.js"
    testcase = Path.home() / "robobisect" / "tests" / "bwo" / "203406.js"
    if not testcase.is_file():
        raise IOError(f"Testcase not found at: {testcase}")  # Comment out if testing for (compilation)

    wkrepo = Gitrepo("git.webkit.org/WebKit", Path.home() / "webkit")
    wkrepo.start_bisect()

    # after_rev = "8d9cc91e1b379f3560b56ce031aabf38b7b7a559"  # Bug 187947
    # after_rev = "eb42a8967d53ebb95bd59b6d89662ac7fdf95a8b"  # master as of 20200420
    after_rev = "409a450e5645c974b3a7f40486fd114d676c99d8"  # Bug 203406
    wkrepo.compile(after_rev)
    after_result = wkrepo.test(after_rev, runtime_params=[
        "--useDFGJIT=true", "--forceEagerCompilation=true", testcase,
    ])
    wkrepo.set_bisect_result(after_rev, after_result)

    # When checking in GitHub, the earliest known working revision hash is:
    # Ubuntu 18.04:
    #   868adfcb9efa4ad5cf4d0ddd5a772e5bdb2f3f35
    #   Corresponding hash on a local checkout: 011c994d52cc30bdec69aebed8ec1a025966b34a
    # before_rev = "aeae9db386ded44baf96a7bd15e5a278cdb531c2"  # Bug 187947
    # before_rev = "011c994d52cc30bdec69aebed8ec1a025966b34a"
    before_rev = "167a380488fc129bb796f025e5848dc7844d82e0"  # Bug 203406
    wkrepo.compile(before_rev)
    before_result = wkrepo.test(before_rev, runtime_params=[
        "--useDFGJIT=true", "--forceEagerCompilation=true", testcase,
    ])
    if before_result == after_result:
        wkrepo.reset_bisect()
        raise ValueError(f"Both start and end revs show: {after_result}")

    updated_rev, bisect_output = wkrepo.set_bisect_result(before_rev, before_result)

    while "left to test after this" in bisect_output:  # Note that this message is in stderr
        wkrepo.compile(updated_rev)
        updated_result = wkrepo.test(updated_rev, runtime_params=[
            "--useDFGJIT=true", "--forceEagerCompilation=true", testcase,
        ])
        updated_rev, bisect_output = wkrepo.set_bisect_result(updated_rev, updated_result)

    wkrepo.reset_bisect()
