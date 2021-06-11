
### Run RE-ALINE against Excel data

```bash
mkdir {input,output}
```

Move your Excel input data into `input/` as `input.xlsx` and run the following command:

```bash
docker run -it --rm "parsertongue/re-aline:latest" re-aline-excel-data --input /app/input.xlsx --output /app/output.xlsx
```
