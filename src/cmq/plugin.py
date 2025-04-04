from importlib import metadata


class ResourceLoader:

    def __getattr__(self, attr: str) -> "ResourcePlugin":
        resource_class = PluginManager().get_resource_class(attr)
        resource_instance = resource_class(self)
        return resource_instance


class ResourcePlugin(ResourceLoader):
    pass


class SessionPlugin(ResourceLoader):
    pass



class PluginManager:

    def __init__(self, group: str = "cmq.provider.aws"):
        self.group = group
        self.sessions: dict[str, SessionPlugin] = {}
        self.resources: dict[str, ResourcePlugin] = {}
        self.load()

    def load(self):
        entry_points = list(metadata.entry_points(group=self.group))
        for ep in entry_points:
            plugin = ep.load()
            if issubclass(plugin, SessionPlugin):
                self.sessions[ep.name] = plugin
            elif issubclass(plugin, ResourcePlugin):
                self.resources[ep.name] = plugin
            else:
                raise ValueError(f"Unknown plugin subclass type: {ep.name}")

    def get_sessions(self) -> dict[str, SessionPlugin]:
        return self.sessions

    def get_resources(self) -> dict[str, ResourcePlugin]:
        return self.resources

    def get_session_class(self, name: str) -> SessionPlugin:
        if name in self.sessions:
            return self.sessions[name]
        raise ValueError(f"Unknown session class {name}")

    def get_resource_class(self, name: str) -> ResourcePlugin:
        if name in self.resources:
            return self.resources[name]
        raise ValueError(f"Unknown resource class {name}")