import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

QRC_USERNAME = os.getenv("QRC_USERNAME")
QRC_PASSWORD = os.getenv("QRC_PASSWORD")
CORE_IP_ADDRESS = os.getenv("CORE_IP_ADDRESS")
UCI_SCRIPT_COMPONENTS = []
CONTROL_SCRIPT_COMPONENTS = ["dev"]


def uci_scripts(
    components: list[str] = UCI_SCRIPT_COMPONENTS, control: str = "code"
) -> list[dict[str, Any]]:
    scripts = []
    for component in components:
        script = {
            "component": component,
            "control": control,
        }
        scripts.append(script)
    return scripts


def control_scripts(
    components: list[str] = CONTROL_SCRIPT_COMPONENTS, control: str = "code"
) -> list[dict[str, Any]]:
    scripts = []
    for component in components:
        script = {
            "component": component,
            "control": control,
            "filepath": f"/Users/aconover/Documents/Development/qsys/dev-utils/lua/scripts/{component}.lua",
        }
        scripts.append(script)
    return scripts
