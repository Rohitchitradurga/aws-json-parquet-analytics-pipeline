# Local Development

Tools for running the pipeline on your machine.

- `docker-compose.yml`: Spins up local Postgres and OpenSearch for testing loaders.
- `runner.py`: A utility script to generate fake data, run the transformation logic, and verify the output.

## Setup
Run `./tools/setup_local.sh` to create a virtual environment and install dependencies.
Then run `source .venv/bin/activate` before running the runner.

