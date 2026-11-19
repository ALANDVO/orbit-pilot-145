import sys
sys.path.insert(0, '.')

from vm.engine import VMEngine


def test_vm_creation():
    """Test that VM can be created with specified config."""
    vm = VMEngine(config={"name": "test-vm", "memory_mb": 512, "cpu_count": 2})
    assert vm.id == "test-vm"
    assert vm.state == "created"
    assert vm.config == {"name": "test-vm", "memory_mb": 512, "cpu_count": 2}


def test_vm_start():
    """Test that VM can be started."""
    vm = VMEngine(config={"name": "start-vm"})
    assert vm.state == "created"
    result = vm.start()
    assert result["state"] == "running"
    assert result["id"] == "start-vm"


def test_vm_stop():
    """Test that VM can be stopped after starting."""
    vm = VMEngine(config={"name": "stop-vm"})
    vm.start()
    assert vm.state == "running"
    result = vm.stop()
    assert result["state"] == "stopped"


def test_vm_cannot_start_when_running():
    """Test that starting a running VM raises RuntimeError."""
    vm = VMEngine(config={"name": "error-vm"})
    vm.start()
    try:
        vm.start()
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "Cannot start VM" in str(e)


def test_vm_cannot_stop_when_stopped():
    """Test that stopping a stopped VM raises RuntimeError."""
    vm = VMEngine(config={"name": "error-vm2"})
    try:
        vm.stop()
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "Cannot stop VM" in str(e)


def test_vm_reset():
    """Test that VM can be reset to created state."""
    vm = VMEngine(config={"name": "reset-vm"})
    vm.start()
    vm.stop()
    result = vm.reset()
    assert result["state"] == "created"


def test_vm_get_status():
    """Test that VM status can be retrieved."""
    vm = VMEngine(config={"name": "status-vm", "memory_mb": 1024})
    status = vm.get_status()
    assert status["id"] == "status-vm"
    assert status["state"] == "created"
    assert status["config"]["memory_mb"] == 1024
