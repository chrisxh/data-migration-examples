# data-migration-examples
examples of data migration to Careerleaf platform using [Careerleaf public API](https://github.com/Careerleaf/api)


## Configuration 

copy `config.ini.sample` to `config.ini` and add correct CL API keys and target system url


## Employers migration 

Migration from XML file as data source
see [employers/employer.py](https://github.com/Careerleaf/data-migration-examples/blob/master/employers/employers.py) 

xml data used - [sample](https://github.com/Careerleaf/data-migration-examples/blob/master/employers/data_sample.xml)

  python runner.py employers



## Job seekers data export 

  python runner.py jobseekers-export

