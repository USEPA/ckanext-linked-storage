[![Tests](https://github.com/USEPA/ckanext-linked-storage/workflows/Tests/badge.svg?branch=main)](https://github.com/USEPA/ckanext-linked-storage/actions)

# ckanext-linked-storage

CKAN extension enabling files accessible via a mounted network share to be created as dataset resources with CKAN acting as a proxy. 


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8 and earlier | not tested    |
| 2.9             | yes           |


## Installation

To install ckanext-linked-storage:

1. Activate your CKAN virtual environment, for example:
```
. /usr/lib/ckan/default/bin/activate
```   
    

2. Clone the source and install it on the virtualenv:
```
    git clone https://github.com/USEPA/ckanext-linked-storage.git    
    cd ckanext-linked-storage    
    pip install -e .    
```
3. Add `linked_storage` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

4. Add storage locations via `ckanext.linked_storage.mountpoints` and 
   `ckanext.linked_storage.net_paths` in the CKAN config file


5. Restart CKAN


## Adding resources using linked storage

To create a resource using this functionality via the API `call resource_create` with `url_type = 'link-storage'` and 
provide the path to the resource either as the `url` or `link_path`. An example can be seen below:
```python
resource_create(package_id='some package', name='a linked resource package', url_type='link-storage', link_path="\\some-host\share\linked_file.csv" )
```
    

## Config settings

To connect resources using the linked storage system the available mounted resources need to be defined. This is done using two of the configuration inputs.

| Config Input                        |  Description                                                                                          |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
|`ckanext.linked_storage.mountpoints` | Specifies the mountpoints, or folders where the data files can be accessed in a space delimited list. |
|`ckanext.linked_storage.net_paths`   | Specifies paths which are used to match provided resource paths to the corresponding mountpoint.      |


## Developer installation

To install ckanext-linked-storage for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/USEPA/ckanext-linked-storage.git
    cd ckanext-linked-storage
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

No tests are currently configured

To run the tests, do:

    pytest --ckan-ini=test.ini

## Disclaimer

The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis
and the user assumes responsibility for its use.  EPA has relinquished control of the information and no longer
has responsibility to protect the integrity , confidentiality, or availability of the information.  Any
reference to specific commercial products, processes, or services by service mark, trademark, manufacturer,
or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA.  The EPA seal
and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or
the United States Government.
