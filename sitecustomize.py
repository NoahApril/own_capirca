"""Project-wide site customizations."""

import os

# Disable auto-loading of external pytest plugins to ensure deterministic runs.
os.environ.setdefault('PYTEST_DISABLE_PLUGIN_AUTOLOAD', '1')
