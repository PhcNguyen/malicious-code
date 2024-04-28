import os
import subprocess

from google.auth import _helpers
from google.auth import environment_vars
from google.auth import exceptions



_CONFIG_DIRECTORY = "gcloud"

_WINDOWS_CONFIG_ROOT_ENV_VAR = "APPDATA"


_CREDENTIALS_FILENAME = "application_default_credentials.json"

_CLOUD_SDK_POSIX_COMMAND = "gcloud"
_CLOUD_SDK_WINDOWS_COMMAND = "gcloud.cmd"

_CLOUD_SDK_CONFIG_GET_PROJECT_COMMAND = ("config", "get", "project")

_CLOUD_SDK_USER_ACCESS_TOKEN_COMMAND = ("auth", "print-access-token")

CLOUD_SDK_CLIENT_ID = (
    "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com"
)


def get_config_path():
    """Returns the absolute path the the Cloud SDK's configuration directory.

    Returns:
        str: The Cloud SDK config path.
    """
    
    try:
        return os.environ[environment_vars.CLOUD_SDK_CONFIG_DIR]
    except KeyError:
        pass

    
    if os.name != "nt":
        return os.path.join(os.path.expanduser("~"), ".config", _CONFIG_DIRECTORY)
    
    else:
        try:
            return os.path.join(
                os.environ[_WINDOWS_CONFIG_ROOT_ENV_VAR], _CONFIG_DIRECTORY
            )
        except KeyError:
            
            
            drive = os.environ.get("SystemDrive", "C:")
            return os.path.join(drive, "\\", _CONFIG_DIRECTORY)


def get_application_default_credentials_path():
    """Gets the path to the application default credentials file.

    The path may or may not exist.

    Returns:
        str: The full path to application default credentials.
    """
    config_path = get_config_path()
    return os.path.join(config_path, _CREDENTIALS_FILENAME)


def _run_subprocess_ignore_stderr(command):
    """ Return subprocess.check_output with the given command and ignores stderr."""
    with open(os.devnull, "w") as devnull:
        output = subprocess.check_output(command, stderr=devnull)
    return output


def get_project_id():
    """Gets the project ID from the Cloud SDK.

    Returns:
        Optional[str]: The project ID.
    """
    if os.name == "nt":
        command = _CLOUD_SDK_WINDOWS_COMMAND
    else:
        command = _CLOUD_SDK_POSIX_COMMAND

    try:
        
        
        project = _run_subprocess_ignore_stderr(
            (command,) + _CLOUD_SDK_CONFIG_GET_PROJECT_COMMAND
        )

        
        project = _helpers.from_bytes(project).strip()
        return project if project else None
    except (subprocess.CalledProcessError, OSError, IOError):
        return None


def get_auth_access_token(account=None):
    """Load user access token with the ``gcloud auth print-access-token`` command.

    Args:
        account (Optional[str]): Account to get the access token for. If not
            specified, the current active account will be used.

    Returns:
        str: The user access token.

    Raises:
        google.auth.exceptions.UserAccessTokenError: if failed to get access
            token from gcloud.
    """
    if os.name == "nt":
        command = _CLOUD_SDK_WINDOWS_COMMAND
    else:
        command = _CLOUD_SDK_POSIX_COMMAND

    try:
        if account:
            command = (
                (command,)
                + _CLOUD_SDK_USER_ACCESS_TOKEN_COMMAND
                + ("--account=" + account,)
            )
        else:
            command = (command,) + _CLOUD_SDK_USER_ACCESS_TOKEN_COMMAND

        access_token = subprocess.check_output(command, stderr=subprocess.STDOUT)
        
        return access_token.decode("utf-8").strip()
    except (subprocess.CalledProcessError, OSError, IOError) as caught_exc:
        new_exc = exceptions.UserAccessTokenError(
            "Failed to obtain access token", caught_exc
        )
        raise new_exc from caught_exc
