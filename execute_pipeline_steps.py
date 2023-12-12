#!/bin/env python3
"""
SYNOPSIS:
    ./execute_pipeline_steps.py FILE JOBID STEPNAME [...STEPNAME]

    Run what's found at the given location in the pipeline yaml.  This lets us keep
    the local run and the pipeline build in step: the yaml is the single source of truth.

"""

import subprocess
import sys
import yaml


if __name__ == "__main__":
    file_name = sys.argv[1]
    job_name = sys.argv[2]
    step_names = sys.argv[3:]

    with open(file_name, "r") as fp:
        pipeline_config = yaml.safe_load(fp)

    step_list = pipeline_config["jobs"][job_name]["steps"]
    step_dict = {item["name"]: item for item in step_list}

    status_latch = 0
    for name in step_names:
        command = step_dict[name]["run"]
        print(f"{name}: {command}")
        completed = subprocess.run(command, shell=True)
        status_latch = status_latch or completed.returncode
        print(f"return status: {completed.returncode}")

    if status_latch:
        raise SystemError("Error: not all steps completed smoothly.")
