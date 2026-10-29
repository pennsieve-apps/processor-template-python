# Pennsieve app template (Python)

A starting point for an app that runs as a step in Pennsieve workflows. It
reads the files it is given, does its work, and writes results; Pennsieve
takes care of moving data in and out, running it on the right compute, and
showing what happened.

Pennsieve's **Publish an app** creates a repository from this template with
your app's `app.yml` already written. Starting here by hand works too: use
**Use this template** on GitHub, then edit `app.yml`.

## Where to put the work

`processor/main.py`, in `main()`. It is run with:

| Variable | Holds |
|---|---|
| `INPUT_DIR` | the folder with the step's input files |
| `OUTPUT_DIR` | the folder to write to; each output in `app.yml` is its own subfolder, `OUTPUT_DIR/<output>/` |
| each parameter in `app.yml` | its value for this run, as an environment variable of the same name |

Return `0` when done. Anything else fails the step, and whatever you logged
is in the run's log.

Add Python packages to the `Dockerfile` (`pip install`), and files you need
next to the code under `processor/`.

## `app.yml`

What the App Store shows and what a workflow needs: the app's name and
description, its compute types and size, its parameters, its inputs and
outputs. Edit it here or in the app's page in Pennsieve (**Update in
builder**).

## Runtimes

The image serves every compute type (`processor/entry.py`): as an ECS task
(`standard`, `gpu`) it runs `main()` once; as a Lambda function (`lambda`) it
serves `processor/handler.py`, which sets the same variables from the
function's payload and runs the same `main()`. Add `lambda` to
`computeTypes` for an app that finishes within 15 minutes and 10 GB: it
starts in seconds instead of the minute an ECS task takes.

## Running it locally

```
make test   # with Python, over sample-input/, into data/output/
make run    # in Docker, the way Pennsieve runs it
```

## Publishing

1. The Pennsieve GitHub App must be installed on the repository (Pennsieve
   asks for that when you publish).
2. Create a release on GitHub, `v0.1.0` for the first one, or publish it from
   the app's page in Pennsieve. Pennsieve builds the image and the app is in
   the App Store when the build is done.

Every later release is a new version of the app; workflows pin the version
they use.
