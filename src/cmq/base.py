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
        self._pipeline = []

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
        Adds a selection operation to the pipeline that will select the specified attributes.

        Args:
            *args (list[str]): The attributes to be selected.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._pipeline.append(lambda resources, context: [
            {key: self._safe_key(r, key) for key in args} if isinstance(r, dict) else r
            for r in resources
        ])
        return self

    def filter(self, func: callable) -> "ResourceInterface":
        """
        Adds a filter operation to the pipeline that will filter resources based on the given function.

        Args:
            func (callable): The filter function to be added.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_filter(func, r)
        ])
        return self

    def transform(self, key: str, func: callable) -> "ResourceInterface":
        """
        Adds a transformation operation to the pipeline that will transform the specified attribute.

        Args:
            key (str): The key of the attribute to transform.
            func (callable): The transformation function to be added.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._pipeline.append(lambda resources, context: [
            {**r, key: func(r.get(key)) if key in r else None} if isinstance(r, dict) else r
            for r in resources
        ])
        return self

    def calculate(self, key: str, func: callable) -> "ResourceInterface":
        """
        Adds a calculation operation to the pipeline that will calculate a new attribute.

        Args:
            key (str): The new key of the attribute.
            func (callable): The calculation function to be used.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._pipeline.append(lambda resources, context: [
            {**r, key: func(r)} if isinstance(r, dict) else r
            for r in resources
        ])
        return self

    def _safe_filter(self, func: callable, resource: dict) -> bool:
        with suppress(AttributeError, KeyError, TypeError):
            return func(resource)
        return False

    def _safe_key(self, resource: dict, key: str) -> Any:
        """
        Safely retrieves a value from a resource dictionary using the benedict library.

        Args:
            resource (dict): The resource dictionary.
            key (str): The key to retrieve.

        Returns:
            Any: The value associated with the key, or None if not found.
        """
        with suppress(AttributeError, KeyError, ValueError):
            return benedict(resource).get(key)
        return None

    def _process_pipeline(self, resources: list, context: dict) -> list:
        """
        Processes the resources through all pipeline operations.

        Args:
            resources (list): The list of resources to process.
            context (dict): The context containing session information.

        Returns:
            list: The processed resources after applying all pipeline operations.
        """
        for operation in self._pipeline:
            resources = operation(resources, context)
        return resources

    def eq(self, key, value) -> "ResourceInterface":
        """
        Adds an equality filter to the resource.

        Args:
            key (str): The key of the attribute to compare.
            value (Any): The value to compare against.

        Returns:
            ResourceInterface: The updated resource object.
        """
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key) == value
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key) != value
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key) in value
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if value in self._safe_key(r, key)
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if value not in self._safe_key(r, key)
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key).startswith(value)
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key).endswith(value)
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key) > value
        ])
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
        self._pipeline.append(lambda resources, context: [
            r for r in resources if self._safe_key(r, key) < value
        ])
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