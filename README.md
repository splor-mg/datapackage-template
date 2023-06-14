# datapackage-template

```
docker build --tag dp .
docker run -it --rm --mount type=bind,source=$(PWD),target=/project dp bash
python scripts/extract.py acoes_planejamento
```
