#!/bin/bash
# add docker neo4j setup
export PYTHONPATH=$(pwd)
uvicorn src.main:app --host 0.0.0.0 --port 8000
