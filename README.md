# data-migration-examples
examples of data migration to Careerleaf platform using [Careerleaf public API](https://github.com/Careerleaf/api)


## Configuration 
Prerequisites:

Python 3.5+
```
  python -m pip install pyyaml --user
  python -m pip install requests --user
```

copy `config.ini.sample` to `config.ini` and add correct CL API keys and target system url

For XML import of employers
```
  python -m pip install lxml --user
```

For CSV import of employers
```
  python -m pip install pandas --user
```


## Employers migration

Migration from XML file as data source
see [employers/importer.py](https://github.com/Careerleaf/data-migration-examples/blob/master/employers/importer.py) 

xml data used - [sample](https://github.com/Careerleaf/data-migration-examples/blob/master/employers/data_sample.xml)

  `python runner.py employers-import-xml`


Migration from CSV file as data source
see [employers/importer_csv.py](https://github.com/Careerleaf/data-migration-examples/blob/master/employers/importer_csv.py) 

csv data used - [sample](https://github.com/Careerleaf/data-migration-examples/blob/master/employers/data_sample.csv)

  `python runner.py employers-import-csv`



## Job seekers data export 

  python runner.py jobseekers-export

