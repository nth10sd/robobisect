"""Class to create compile_binary objects."""

from pathlib import Path
import subprocess

from robobisect.util.utils import RUN_LOG


class Shell:  # pylint: disable=missing-class-docstring
    def __init__(self):
        self.jsc_bin_path = None

    def compile(self):  # pylint: disable=missing-function-docstring,missing-return-doc,missing-return-type-doc
        wk_repo_dir = Path.home() / "webkit"
        assert not (wk_repo_dir / "WebKitBuild").is_dir()

        compile_cmd_working_dir = wk_repo_dir / "Tools" / "Scripts"
        subprocess.run(
            [compile_cmd_working_dir / "build-webkit", "--jsc-only", "--debug"],
            check=False, cwd=wk_repo_dir,
            # env=dict(os.environ, LD_LIBRARY_PATH=str(wk_repo_dir / "WebKitBuild" / "Debug" / "lib")),
        )

        self.jsc_bin_path = wk_repo_dir / "WebKitBuild" / "Debug" / "bin" / "jsc"
        # assert self.jsc_bin_path.is_file()  # Commented out for checking if binary exists
        return self.jsc_bin_path

    def test(self, runtime_params):  # pylint: disable=missing-function-docstring
        RUN_LOG.info(self.jsc_bin_path)
        RUN_LOG.info(runtime_params)
