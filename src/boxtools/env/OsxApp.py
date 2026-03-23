import subprocess
import textwrap
from pathlib import Path
from typing import Optional


class OsxApp:
    """
    Represents a macOS application (e.g., 'iTerm2', 'iTerm', 'Finder').
    Provides helpers to check existence and interact via AppleScript.
    """

    def __init__(self, app_name: str):
        """
        :param app_name: Application name as shown in /Applications, without '.app'
                         e.g. 'iTerm2', 'iTerm', 'Finder'
        """
        self.app_name = app_name

    # ---------- Generic helpers ----------

    def exists(self) -> bool:
        """
        Check if the app bundle exists in common locations.
        """
        candidates = [
            Path("/Applications") / f"{self.app_name}.app",
            Path.home() / "Applications" / f"{self.app_name}.app",
            ]
        return any(p.exists() for p in candidates)

    def _quote_applescript(self, s: str) -> str:
        """
        Quote a Python string for safe use in an AppleScript string literal.
        """
        return '"' + s.replace('"', '\\"') + '"'

    def _run_applescript(self, script: str) -> None:
        """
        Run the provided AppleScript via osascript.
        Raises subprocess.CalledProcessError on failure.
        """
        subprocess.run(["osascript", "-e", script], check=True)

    # ---------- iTerm-specific convenience ----------

    def open_iterm_tab(self, command: Optional[str] = None, force_tab: bool = False) -> None:
        """
        Open a new tab in iTerm/iTerm2 and optionally run a shell command.

        This method assumes this OsxApp instance represents iTerm or iTerm2
        (i.e., app_name is 'iTerm' or 'iTerm2').

        :param force_tab: to force opening a tab even if no window is detected
        :param command: Shell command to execute in the new tab; if None, just opens a blank tab.
        :raises RuntimeError: if the app is not found.
        :raises subprocess.CalledProcessError: if osascript fails.
        """
        if not self.exists():
            raise RuntimeError(
                f"{self.app_name}.app not found in /Applications or ~/Applications. "
                f"Please check the app name and installation."
            )

        command_line = (
            f"write text {self._quote_applescript(command)}"
            if command
            else ""
        )

        # AppleScript:
        # - Activates the app
        # - If there is no window, creates one and runs the command in its first session
        # - Otherwise, creates a new tab in the current window and runs the command there
        script = textwrap.dedent(f"""
        tell application "{self.app_name}"
            activate
            if ((count of windows) is 0) and ({str(not force_tab).lower()}) then
                set newWindow to (create window with default profile)
                tell current session of newWindow
                    {command_line}
                end tell
            else
                tell current window
                    create tab with default profile
                    tell current session
                        {command_line}
                    end tell
                end tell
            end if
        end tell
        """)

        self._run_applescript(script)
