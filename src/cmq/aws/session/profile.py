import boto3
import botocore
import os
import sys
import configparser

from typing import Any
from cmq.base import Session


class profile(Session):

    def __init__(self, parent: object=None, name: str | None = None, **kwargs: dict[str, Any]):
        """
        Initialize a new Profile object.

        Args:
            parent (object): The parent object. Defaults to None.
            name (str | None): The name of the profile. Defaults to None.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(parent)
        self._name = name
        self._list_attr = ["id", "name", "region"]
        self._list_parameters = kwargs
        self.config_path = os.path.expanduser(os.getenv("AWS_CONFIG_FILE", "~/.aws/config"))

    def get_profiles(self) -> tuple:
        config = configparser.ConfigParser()
        config.read([self.config_path])
        return config, config.sections() if self._name is None else [f"profile {self._name}"]

    def get_profile_name(self, profile: str) -> str:
        return profile.split()[-1] if profile.startswith("profile ") else profile

    def get_session_context(self, profile: dict) -> dict:
        return {
            "session_resource": profile,
            "session_name": profile["name"],
            "aws_region": profile.get("region"),
            "aws_session": self.get_session(profile),
        }

    def get_sessions(self):
        with self.context("[bold green]Getting profile list..."):
            config, profiles = self.get_profiles()
            sessions = [{"name": self.get_profile_name(profile), **config[profile]} for profile in profiles]
            return self._get_attr(self._exclude(sessions))

    def get_session(self, profile: dict) -> boto3.Session:
        try:
            return boto3.Session(profile_name=profile["name"])
        except botocore.exceptions.ProfileNotFound:
            profile_name = profile["name"]
            sys.stderr.write(f"Profile {profile_name} not found.\n")

    def _list(self, results, context) -> None:
        results.append(context["session_resource"])

    def _dict(self, results, context) -> None:
        profile_list = results.setdefault(context["session_name"], [])
        profile_list.append(context["session_resource"])
