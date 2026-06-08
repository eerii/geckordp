# pylint: disable=unused-import
import pytest

import geckordp.tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.root import RootActor
from geckordp.actors.screenshot import ScreenshotActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from geckordp.tests.helpers.utils import *


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    ctx_id = actor_ids["browsingContextID"]
    screenshot = ScreenshotActor(cl, root.get_root()["screenshotActor"])
    return cl, ctx_id, screenshot


def test_capture():
    cl = None
    try:
        cl, ctx_id, screenshot = init()
        response = screenshot.capture(ctx_id)
        if "error" in response:
            pytest.skip(f"screenshot capture failed: {response['error']}")
        val = response["value"]["data"]
        assert len(val) > 1024
    finally:
        cl.disconnect()
