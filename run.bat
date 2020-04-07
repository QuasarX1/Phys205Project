@echo off
call conda activate Phys205 && (
  python run.py %*
  (call )
) || (
  echo Unable to run simulation due to missing conda environment!
  call create_environment
  exit
)