from geckordp.actors.actor import Actor


class WebExtensionActor(Actor):
    """https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/webextension.js"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def reload(self):
        return self.client.send_receive({"to": self.actor_id, "type": "reload"})

    def terminate_background_script(self):
        return self.client.send_receive(
            {"to": self.actor_id, "type": "terminateBackgroundScript"}
        )

    def reload_descriptor(self, bypass_cache=False):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "reloadDescriptor",
                "bypassCache": bypass_cache,
            }
        )

    def get_watcher(self, is_server_target_switching_enabled=False):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getWatcher",
                "isServerTargetSwitchingEnabled": is_server_target_switching_enabled,
            }
        )

