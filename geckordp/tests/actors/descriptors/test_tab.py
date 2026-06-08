# pylint: disable=unused-import
import pytest

import geckordp.tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.root import RootActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from geckordp.tests.helpers.utils import *


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    return cl, tab


def test_get_target():
    cl = None
    try:
        cl, tab = init()
        actor_ids = tab.get_target()
        val = actor_ids["consoleActor"]
        assert "consoleActor" in val
    finally:
        cl.disconnect()


def test_get_favicon():
    cl = None
    try:
        cl, tab = init()
        val = tab.get_favicon().get("favicon", 0)
        assert val != 0
    finally:
        cl.disconnect()


def test_get_watcher():
    cl = None
    try:
        cl, tab = init()
        val = tab.get_watcher()["actor"]
        assert "watcher" in val
    finally:
        cl.disconnect()


def test_navigate_to():
    cl = None
    try:
        cl, tab = init()
        val = tab.navigate_to("https://example.com/")
        assert response_valid("tabDescriptor", val), str(val)
    finally:
        cl.disconnect()


def test_go_back():
    cl = None
    try:
        cl, tab = init()
        val = tab.go_back()
        assert response_valid("tabDescriptor", val), str(val)
    finally:
        cl.disconnect()


def test_go_forward():
    cl = None
    try:
        cl, tab = init()
        val = tab.go_forward()
        assert response_valid("tabDescriptor", val), str(val)
    finally:
        cl.disconnect()


def test_reload_descriptor():
    cl = None
    try:
        cl, tab = init()
        val = tab.reload_descriptor()
        assert response_valid("tabDescriptor", val), str(val)
    finally:
        cl.disconnect()
