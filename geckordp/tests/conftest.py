# pylint: disable=unused-import,wrong-import-position
import logging
import os
import socket
import subprocess
import sys
import time
from functools import partial
from subprocess import Popen

import pytest

from geckordp.firefox import Firefox
from geckordp.logger import log, set_stdout_log_level, wlog
from geckordp.profile import ProfileManager
from geckordp.settings import GECKORDP
from geckordp.utils import kill

import geckordp.tests.helpers.constants as constants
from geckordp.tests.helpers.utils import is_port_open


FIREFOX_ONLY_DIRS = [
    "actors/addon",
    "actors/accessibility",
]

FIREFOX_ONLY_FILES = [
    "test_profile.py",
    "actors/test_preference.py",
    "actors/test_device.py",
    "actors/test_memory.py",
    "actors/test_heap_snapshot.py",
]


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["firefox", "external"], default="firefox")
    parser.addoption("--remote-port", type=int, default=6100)


def pytest_ignore_collect(collection_path, config):
    if config.getoption("--browser", default="firefox") != "external":
        return None
    path_str = str(collection_path)
    for skip_dir in FIREFOX_ONLY_DIRS:
        if skip_dir in path_str:
            return True
    for skip_file in FIREFOX_ONLY_FILES:
        if path_str.endswith(skip_file):
            return True
    return None


def dispose(handle: Popen | None, pm: ProfileManager | None):
    log("tests finished")
    if handle is not None:
        kill(handle)
        if pm is not None:
            pm.remove(constants.PROFILE0)
            pm.remove(constants.PROFILE1)
            pm.remove(constants.PROFILE2)
        try:
            handle.wait(5.0)
        except Exception:
            pass


def _get_worker_id(config):
    if hasattr(config, "workerinput"):
        return config.workerinput["workerid"]
    return "master"


def _is_xdist_controller(config):
    return config.pluginmanager.hasplugin("xdist") and not hasattr(
        config, "workerinput"
    )


@pytest.fixture(scope="session", autouse=True)
def initialize(request):
    browser = request.config.getoption("--browser")
    pm = None
    handle = None

    capmanager = request.config.pluginmanager.getplugin("capturemanager")
    with capmanager.global_and_fixture_disabled():
        set_stdout_log_level(logging.DEBUG)
        GECKORDP.DEBUG_REQUEST = 1
        GECKORDP.DEBUG_RESPONSE = 1

        if browser == "firefox":
            pm = ProfileManager()
            if not is_port_open(constants.REMOTE_HOST, constants.REMOTE_PORT):
                pm.remove(constants.PROFILE0)
                pm.remove(constants.PROFILE1)
                pm.remove(constants.PROFILE2)
                log(f"initialize profile '{constants.PROFILE0}'")
                profile = pm.create(constants.PROFILE0)
                profile.set_required_configs()

                log(
                    f"start firefox with debug server on {constants.REMOTE_HOST}:{constants.REMOTE_PORT}"
                )
                handle = Firefox.start(
                    "https://example.com/",
                    port=constants.REMOTE_PORT,
                    profile=constants.PROFILE0,
                    append_args=["-headless"],
                    auto_kill=False,
                )
            else:
                wlog(
                    f"{constants.REMOTE_HOST}:{constants.REMOTE_PORT} already in use"
                )

        if browser == "external":
            if _is_xdist_controller(request.config):
                return

            worker_id = _get_worker_id(request.config)
            base_port = request.config.getoption("--remote-port", 6100)
            if worker_id == "master":
                port = base_port
            else:
                worker_num = int(worker_id.replace("gw", ""))
                port = base_port + worker_num
            constants.REMOTE_PORT = port

        request.addfinalizer(partial(dispose, handle, pm))
