import json


class Qrc:
    """
    QRC is a Unicode-based TCP/IP control protocol. The client connects to the Q-SYS Core (or emulator) on port 1710 and sends JSON RPC 2.0 null-terminated commands.

    TODO: Implement Change Group Methods
    """

    def __init__(self):
        pass

    def logon(self, id: int, username: str, password: str) -> str:
        """
        Type: Connection Method
        Name: Logon
        Description: Logs on to the system.
        """
        data = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "Logon",
            "params": {
                "User": username,
                "Password": password,
            },
        }
        return json.dumps(data)

    def no_op(self) -> str:
        """
        Type: Connection Method
        Name: NoOp
        Description: This is a simple, "do nothing" method for making sure that the socket remains open.
        """

        data = {"jsonrpc": "2.0", "method": "NoOp", "params": {}}
        return json.dumps(data)

    def get_status(self, id: int) -> str:
        """
        Type: Status Method
        Name: StatusGet
        Description: Manually request the current status. Returns the EngineStatus of the Q-SYS Core.
        """

        data = {"jsonrpc": "2.0", "id": id, "method": "StatusGet", "params": 0}
        return json.dumps(data)

    def get_control(self, id: int, controls: list[str]) -> str:
        """
        Type: Control Method
        Name: Control.Get
        Description: Specify an array of Named Control strings, receive an array of control values.
        """

        data = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "Control.Get",
            "params": [controls],
        }
        return json.dumps(data)

    def set_control(self, id: int, control: str, value: str) -> str:
        """
        Type: Control Method
        Name: Control.Set
        Description: Set a control's value. Specify a single control name, value, and optional ramp time.
        """

        data = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "Control.Set",
            "params": {"control": control, "value": value},
        }
        return json.dumps(data)

    def get_components(self, id: int) -> str:
        """
        Type: Component Control Method
        Name: Components.GetComponents
        Description: Get a list of all named components in a design, along with their type and properties.
        """

        data = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "Components.GetComponents",
        }
        return json.dumps(data)

    def get_component(
        self, id: int, named_component: str, controls: list[dict[str, str]]
    ) -> str:
        """
        Type: Component Control Method
        Name: Component.Get
        Description: Returns the values of one or more specified controls within a specified Named Component.
        """

        data = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "Component.Get",
            "params": {
                "Name": named_component,
                "Controls": controls,
            },
        }
        return json.dumps(data).strip()

    def get_component_controls(self, id: int, control: str) -> str:
        """
        Type: Component Control Method
        Name: Component.GetControls
        Description: Returns a dict of all controls and their values in a specified Named Component.
        """

        data = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "Controls.Get",
            "params": {"Name": control},
        }
        return json.dumps(data)

    def set_component(
        self, id: int, named_component: str, controls: list[dict[str, str]]
    ) -> str:
        """
        Type: Component Control Method
        Name: Component.Set
        Description: Set one or more controls for a single named component. Returns a list of unknown controls after processing.
        """
        data = {
            "jsonrpc": "2.0",
            "method": "Component.Set",
            "id": id,
            "params": {"Name": named_component, "Controls": controls},
        }
        return json.dumps(data)


if __name__ == "__main__":
    ...
