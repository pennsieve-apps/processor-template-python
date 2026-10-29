"""
The Lambda runtime. A Lambda step's payload carries inputDir, outputDir and
the step's parameters as fields (a container gets them as environment
variables); the handler sets those variables and runs the same main(), so
both runtimes do the same work. Nothing to change here when you add a
parameter: every UPPER_CASE field of the payload becomes a variable.
"""
import os
import re

from processor import main as app

PARAMETER = re.compile(r"^[A-Z][A-Z0-9_]*$")


def handler(event, context):
    os.environ["INPUT_DIR"] = event.get("inputDir") or ""
    os.environ["OUTPUT_DIR"] = event.get("outputDir") or ""
    # A warm function keeps its environment between invocations: set this
    # run's parameters, and clear the ones it doesn't set.
    for name in [k for k in os.environ if PARAMETER.match(k) and k not in ("INPUT_DIR", "OUTPUT_DIR")]:
        if name not in event:
            os.environ.pop(name, None)
    for name, value in event.items():
        if PARAMETER.match(name) and value is not None:
            os.environ[name] = str(value).lower() if isinstance(value, bool) else str(value)
    code = app.main()
    if code != 0:
        # An exception fails the step; a returned value would succeed.
        raise RuntimeError(f"the app exited with {code}")
    return {"status": "ok", "outputDir": os.environ["OUTPUT_DIR"]}
