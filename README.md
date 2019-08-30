jira2proj
========================================================================

### Goal 

create script for fast preparation of project plans (xml format) with pre-defined milestones, mandatory tasks and 
check points from JIRA (and other issue trackers in future).

### Input

#### config.py

- path to JIRA ssl certificate
- path to file with Milestones you must have for each feature/story, i.e.:
  * Requirements baselined
  * Access provided
  * Development started
  * Development
  * Development finished
  * etc.
- JIRA fields which will be requested from server

#### config_local.py

- JIRA server host
- JIRA user
- JIRA password
- JIRA filter

### Command line

- There is only one mandatory arg is path to output file specifies with -o path-to-file
- Optional:
  * -m: path to file with milestones
  * -f: path to new property file (*not yet implemented!*)

### Output
XML file compatible with MS proj and OpenProj

### Dependencies
- jira
- lxml
- urllib3

### References

 - https://stackoverflow.com/questions/2415943/what-is-the-xml-spec-for-importing-into-microsoft-project
 - https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2007/bb968733(v=office.12)

### Usage

```bash
$ pip install -r ./requirements.txt
$ python ./jira2proj.py -o output_file
```
