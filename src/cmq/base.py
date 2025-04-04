import csv
import io
import os
from atpbar import flushing
from benedict import benedict
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any
from rich.console import Console
from contextlib import nullcontext, suppress
from cmq.plugin import SessionPlugin
from cmq.plugin import ResourcePlugin


class NodeInterface:

    def __init__(self, parent):
        self._child = None
        self._parent = None
        if parent:
            self._parent = parent
            self._parent._child = self

    def __call__(self):
        return self

    def root(self) -> "ResourceInterface":
        return self._parent.root() if self._parent else self

    def _perform_action(self, action):
        context = {"action": action}
        root = self.root()
        root.traverse(context)

    def traverse(self, context):
        raise NotImplementedError

    def _traverse(self, context):
        if self._child:
            self._child.traverse(context)
        else:
            action = context["action"]
            action(context)


class ResourceInterface(NodeInterface):

    def __init__(self, parent):
        super().__init__(parent)
        self._attrs = []
        self._filters = []
        self._transformed_fields = {}
        self._calculated_fields = {}

    def __call__(self):
        return self

    def root(self) -> "ResourceInterface":
        return self._parent.root() if self._parent else self

    def _perform_action(self, action):
        context = {"action": action}
        root = self.root()
        root.traverse(context)

    def traverse(self, context):
        raise NotImplementedError

    def _traverse(self, context):
        if self._child:
            self._child.traverse(context)
        else:
            action = context["action"]
            action(context)

    def attr(self, *args: list[str]) -> "ResourceInterface":
        """
        Adds the given attributes to the resource.

        Args:
            *args (list[str]): The attributes to be added.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._attrs.extend(args)
        return self

    def filter(self, func: callable) -> "ResourceInterface":
        """
        Adds a filter function to the resource.

        Args:
            func (callable): The filter function to be added.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(func)
        return self

    def transform(self, key: str, func: callable) -> "ResourceInterface":
        """
        Adds a transformation function to the resource.

        Args:
            key (str): The key of the attribute to transform.
            func (callable): The transformation function to be added.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._transformed_fields[key] = func
        return self

    def calculate(self, key: str, func: callable) -> "ResourceInterface":
        """
        Adds a calculation function to the resource.

        Args:
            key (str): The new key of the attribute.
            func (callable): The calculation function to be used.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._calculated_fields[key] = func
        return self

    def _transform(self, resource: dict) -> dict:
        if isinstance(resource, dict):
            for key, func in self._transformed_fields.items():
                resource[key] = func(resource.get(key)) if key in resource else None
        return resource

    def _calculate(self, resource: dict) -> dict:
        if isinstance(resource, dict):
            for key, func in self._calculated_fields.items():
                resource[key] = func(resource)
        return resource

    def _get_attr_from_resource(self, resource) -> Any:
        if self._attrs and isinstance(resource, dict):
            return {key: self._safe_key(resource, key) for key in self._attrs}
        else:
            return resource

    def _get_attr(self, resource_list: list) -> list:
        return [self._get_attr_from_resource(resource) for resource in resource_list]

    def _safe_key(self, resource: dict, key: str) -> Any:
        with suppress(AttributeError, KeyError, ValueError):
            return benedict(resource).get(key)
        return None

    def _safe_filter(self, func: callable, resource: dict) -> bool:
        with suppress(AttributeError, KeyError, TypeError):
            return func(resource)
        return False

    def _exclude(self, resources: list) -> list:
        if self._transformed_fields:
            resources = [self._transform(r) for r in resources]
        if self._calculated_fields:
            resources = [self._calculate(r) for r in resources]

        return [r for r in resources if all(self._safe_filter(f, r) for f in self._filters)]

    def eq(self, key, value) -> "ResourceInterface":
        """
        Adds an equality filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to compare against.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key) == value)
        return self

    def ne(self, key, value) -> "ResourceInterface":
        """
        Adds a not-equal filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to compare against.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key) != value)
        return self

    def in_(self, key, value) -> "ResourceInterface":
        """
        Adds an "in" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (list): The list of values to check for inclusion.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key) in value)
        return self

    def contains(self, key, value) -> "ResourceInterface":
        """
        Adds a "contains" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to check for containment.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: value in benedict(x).get(key))
        return self

    def not_contains(self, key, value) -> "ResourceInterface":
        """
        Adds a "not contains" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to check for non-containment.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: value not in benedict(x).get(key))
        return self

    def starts_with(self, key, value) -> "ResourceInterface":
        """
        Adds a "starts with" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (str): The value to check for starting with.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key).startswith(value))
        return self

    def ends_with(self, key, value) -> "ResourceInterface":
        """
        Adds an "ends with" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (str): The value to check for ending with.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key).endswith(value))
        return self

    def gt(self, key, value) -> "ResourceInterface":
        """
        Adds a "greater than" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to compare against.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key) > value)
        return self

    def lt(self, key, value) -> "ResourceInterface":
        """
        Adds a "less than" filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to compare against.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._filters.append(lambda x: benedict(x).get(key) < value)
        return self

    def context(self, status):
        raise NotImplementedError

    def progress(self, resources):
        raise NotImplementedError


class PagedResourceInterface(ResourceInterface):

    def __init__(self, parent):
        super().__init__(parent)
        self._limit = None

    def _get_pages(self, context) -> Any:
        raise NotImplementedError

    def limit(self, limit: int) -> "PagedResourceInterface":
        """
        Limits the number of resources to be retrieved.

        Args:
            limit (int): The number of resources to be retrieved.

        Returns:
            PagedResourceInterface: The updated resource object.
        """
        self._limit = limit
        return self

    def get_paged_results(self, page) -> list:
        raise NotImplementedError

    def paginate(self, context) -> list:
        resources = []
        for page in self._get_pages(context):
            resources.extend(self.get_paged_results(page))
            if self._limit and len(resources) >= self._limit:
                resources = resources[:self._limit]
                break
        return resources


class Resource(PagedResourceInterface, ResourcePlugin):

    def __init__(self, parent):
        super().__init__(parent)
        self._resource = ""

    def enable_console(self) -> bool:
        return str(os.getenv("CMQ_VERBOSE_OUTPUT", "false")).lower() == "true"

    def list(self) -> list:
        """
        Retrieves a list of resources based on the applied filters.

        Returns:
            list: A list of resource objects.
        """
        results: list = []
        self._perform_action(partial(self._list, results))
        return results

    def dict(self) -> dict:
        """
        Retrieves a dictionary of resources based on the applied filters.

        Returns:
            dict: A dictionary of resource objects.
        """
        results: dict = {}
        self._perform_action(partial(self._dict, results))
        return results

    def csv(self, flat: bool=False) -> str:
        """
        Retrieves a list of resources based on the applied filters and returns them in CSV format.

        Args:
            flat (bool, optional): Specifies whether the dictionaries should be flattened or not. Defaults to False.

        Returns:
            str: List of resources in CSV format.
        """
        results: dict = {}
        self._perform_action(partial(self._dict, results))
        return self._to_csv(results, flat)

    def do(self, action: callable) -> None:
        """
        Performs a custom action on the resources.

        Args:
            action (callable): The action to be performed.
        """
        self._perform_action(action)

    def _list(self, results, context) -> None:
        raise NotImplementedError

    def _dict(self, results, context) -> None:
        raise NotImplementedError

    def _to_csv(self, results, flat: bool) -> str:
        """
        Transform a dictionary of resources into a CSV string in memory
        """
        if not results:
            return ""

        # Get all the keys from the dictionaries
        keys = set({'session'})
        for session, resources in results.items():
            if flat:
                resources = self._flatten(resources)
                results[session] = resources
            keys = self._get_keys_from_dicts(keys, resources)
        keys = sorted(keys)

        # Write the CSV file into memory
        with io.StringIO() as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            for session, resources in results.items():
                dict_writer.writerows(map(lambda r: {"session": session, **r}, resources))
            return output_file.getvalue()

    def _get_keys_from_dicts(self, keys, results) -> set:
        for resource in results:
            keys.update(resource.keys())
        return keys

    def _flatten(self, resources):
        def flatten_dict(resource: dict, parent_resource: dict | None = None, parent_key: str = ""):
            parent_resource = parent_resource or {}
            for key in list(resource.keys()):
                value = resource[key]
                new_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    flatten_dict(value, parent_resource, new_key)
                    del resource[key]
                else:
                    parent_resource[new_key] = value
            return parent_resource
        return [flatten_dict(resource) for resource in resources]


class Session(Resource, SessionPlugin):

    console = Console()

    def context(self, status):
        if self.enable_console():
            return Console().status(status)
        else:
            return nullcontext()

    def get_sessions() -> list:
        raise NotImplementedError

    def get_session_context(self, resource: dict) -> dict:
        """
        Get the session context for the resource. This is a dictionary that will be passed to the traverse function.
        It should contain all the information needed to start a client session.
        The dictionary should contain the following:
        - session_resource: The resource dictionary
        - session_name: The name of the session
        - aws_region: The region of the session
        - aws_account: The account of the session
        - aws_session: The boto3 session object
        """
        raise NotImplementedError

    def traverse(self, context):
        functions = []
        for session in self.get_sessions():
            session_context = self.get_session_context(session)
            session_context.update(context)
            functions.append(partial(self._traverse, session_context))

        with flushing(), ThreadPoolExecutor() as executor:
            running_tasks = [executor.submit(task) for task in functions]
            for running_task in running_tasks:
                running_task.result()

    def _list(self, results, context) -> None:
        results.append(context["session_resource"])