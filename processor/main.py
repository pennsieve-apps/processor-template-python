"""
The app. Pennsieve runs it with:

  INPUT_DIR    the folder with the step's input files
  OUTPUT_DIR   the folder to write results to; each output declared in
               app.yml is its own subfolder, OUTPUT_DIR/<output>/
  parameters   each parameter declared in app.yml, as an environment
               variable of the same name

Exit 0 when done; anything else fails the step, and the log says why.
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("app")
# The Lambda runtime sets the root logger to WARNING before this runs.
log.setLevel(logging.INFO)

# The outputs declared in app.yml.
OUTPUTS = ("results",)


def input_files(input_dir):
    """Every file below INPUT_DIR, relative to it."""
    files = []
    for dirpath, _, filenames in os.walk(input_dir, followlinks=True):
        for name in sorted(filenames):
            files.append(os.path.relpath(os.path.join(dirpath, name), input_dir))
    return sorted(files)


def main():
    input_dir = os.environ.get("INPUT_DIR")
    output_dir = os.environ.get("OUTPUT_DIR")
    example = os.environ.get("EXAMPLE_PARAMETER", "hello")
    if not input_dir or not output_dir:
        log.error("INPUT_DIR and OUTPUT_DIR must be set")
        return 2
    for name in OUTPUTS:
        os.makedirs(os.path.join(output_dir, name), exist_ok=True)

    files = input_files(input_dir)
    log.info("%d input file(s) in %s; EXAMPLE_PARAMETER=%s", len(files), input_dir, example)

    # ------------------------------------------------------------------
    # Your work goes here: read the files under input_dir, write what you
    # make under output_dir/<output>/. This template writes a summary.
    # ------------------------------------------------------------------
    summary = {
        "at": datetime.now(timezone.utc).isoformat(),
        "parameter": example,
        "inputFiles": files,
    }
    with open(os.path.join(output_dir, "results", "summary.json"), "w") as out:
        json.dump(summary, out, indent=2)
    log.info("wrote %s", os.path.join(output_dir, "results", "summary.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
