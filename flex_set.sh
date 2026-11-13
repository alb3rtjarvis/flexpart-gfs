#!/bin/bash

export CPATH=$CPATH:/usr/lib/x86_64-linux-gnu/fortran/gfortran-mod-15:/usr/include:/usr/local/include
export LIBRARY_PATH=/usr/lib:/usr/local/lib
ulimit -s unlimited
export OMP_PLACES=cores
export OMP_PROC_BIND=true
