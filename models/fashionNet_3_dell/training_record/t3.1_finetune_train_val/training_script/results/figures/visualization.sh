#!/bin/bash

rm visualization.log

./visualization.py 2>&1 | tee -a visualization.log