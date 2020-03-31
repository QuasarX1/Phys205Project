@echo off

set answer=n
set /p answer=Would you like to create/update the Phys205 conda environment? [y/N] 
if %answer%==n (exit /B)
if %answer%==N (exit /B)
if %answer%==no (exit /B)
if %answer%==No (exit /B)

call conda activate Phys205 && (
  echo Updating existing environment Phys205:
  call conda env update --name=Phys205 --file=environment.yml
  (call )
) || (
  echo Creating new conda environment Phys205:
  call conda env create --name=Phys205 --file=environment.yml
)

call conda deactivate