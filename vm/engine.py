"""Virtual Machine engine for orbit-pilot-145.

This module provides the core Virtual Machine that bots can use
for task execution and computation.
"""


class VMEngine:
    """The main Virtual Machine engine.

    Attributes:
        config: Configuration dict for the VM.
        state: Current VM state (created, running, stopped, error).
        id: Unique VM identifier.
    """

    # Valid state transitions: from_state -> list of allowed next states
    TRANSITIONS = {
        "created": ["running"],
        "running": ["stopped"],
        "stopped": ["running", "created"],
        "error": [],
    }

    def __init__(self, config: dict = None):
        """Initialize the VM engine with optional config.

        Args:
            config: Dictionary of VM configuration parameters.
                Expected keys: 'name', 'memory_mb', 'cpu_count'.
        """
        self.config = config or {}
        self.state = "created"
        self.id = self.config.get("name", "default-vm")

    def start(self) -> dict:
        """Start the Virtual Machine.

        Returns:
            dict with VM status information.

        Raises:
            RuntimeError: If VM cannot be started from current state.
        """
        allowed = self.TRANSITIONS.get(self.state, [])
        if "running" not in allowed:
            raise RuntimeError(
                f"Cannot start VM in state '{self.state}'; "
                f"expected to transition to one of {allowed}."
            )
        self.state = "running"
        return {
            "id": self.id,
            "state": self.state,
            "message": "VM started successfully",
        }

    def stop(self) -> dict:
        """Stop the Virtual Machine.

        Returns:
            dict with VM status information.

        Raises:
            RuntimeError: If VM cannot be stopped from current state.
        """
        allowed = self.TRANSITIONS.get(self.state, [])
        if "stopped" not in allowed:
            raise RuntimeError(
                f"Cannot stop VM in state '{self.state}'; "
                f"expected to transition to one of {allowed}."
            )
        self.state = "stopped"
        return {
            "id": self.id,
            "state": self.state,
            "message": "VM stopped successfully",
        }

    def reset(self) -> dict:
        """Reset the Virtual Machine to initial state.

        Returns:
            dict with VM status information.
        """
        self.state = "created"
        return {
            "id": self.id,
            "state": self.state,
            "message": "VM reset to created state",
        }

    def get_status(self) -> dict:
        """Get current VM status.

        Returns:
            dict with current VM state and configuration.
        """
        return {
            "id": self.id,
            "state": self.state,
            "config": self.config,
        }
