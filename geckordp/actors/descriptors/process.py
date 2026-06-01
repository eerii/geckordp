from typing import Any, Dict

from geckordp.actors.actor import Actor


class ProcessActor(Actor):
    """https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/process.js"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_target(self, is_browser_toolbox_fission: bool | None = None):
        args: Dict[str, Any] = {
            "to": self.actor_id,
            "type": "getTarget",
        }
        if is_browser_toolbox_fission is not None:
            args["isBrowserToolboxFission"] = is_browser_toolbox_fission
        return self.client.send_receive(args, "process")

    def get_watcher(self, enable_window_global_thread_actors: bool | None = None):
        args: Dict[str, Any] = {
            "to": self.actor_id,
            "type": "getWatcher",
        }
        if enable_window_global_thread_actors is not None:
            args["enableWindowGlobalThreadActors"] = enable_window_global_thread_actors
        return self.client.send_receive(args)

    def reload_descriptor(self, bypass_cache=False):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "reloadDescriptor",
                "bypassCache": bypass_cache,
            }
        )
