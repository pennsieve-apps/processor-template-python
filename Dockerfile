FROM python:3.12-slim

WORKDIR /processor

COPY processor/ /processor/processor/

ENV PYTHONPATH="/processor"

# Runs main() once. On Lambda, Pennsieve's Lambda step runtime runs this same
# entrypoint with the same variables, so the app needs no Lambda code.
ENTRYPOINT ["python3", "-m", "processor.main"]
