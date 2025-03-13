@DEL out\*.sql
@FOR %%i IN (./IN_MDD_CSV/*.csv) DO @python SQLGenerator.py --infile "./IN_MDD_CSV/%%i" --indir ./IN_MAP/ --outdir ./OUT/ --confdir ./CFG/

