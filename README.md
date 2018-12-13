Install requirements
```
pip3 install -r requirements.txt
```

Create registry dir and export env var for prom client
```
export prometheus_multiproc_dir=multiproc-tmp
rm -rf multiproc-tmp && mkdir multiproc-tmp
```

Run uwsgi at foreground (expects correct virtual env dir defined at -H flag)
```
uwsgi --http :5000  --manage-script-name --mount /myapplication=f2:app --enable-threads --processes 5 --plugins python3,http -H .venv
```
