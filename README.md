jira2proj
========================================================================

### Goal 

create script for fast preparation of project plans (xml format) with pre-defined milestones, mandatory tasks and 
check points from JIRA (and other issue trackers in future).
### Usage

```bash
$ pip install -r ./requirements.txt
$ python ./jira2proj.py -o output_file
```
### Input

#### config_local.py
**Note:** You should create file _config_local.py_ in the same dir and add the actual values 
```python
JIRA_SERVER = "https://jira.server.com"
JIRA_LOGIN = "user"
JIRA_PASS = "password"
JIRA_FILTER = "project = PRJ AND issuetype = Feature AND status != Closed AND fixVersion is not EMPTY ORDER BY Rank"
JIRA_SSL_CERT_PATH = "path to crt file with JIRA server ssl certificate"
```

### Command line

- There is only one mandatory arg is path to output file specifies with -o path-to-output-file
- Optional:
  * -m: path to file with milestones
  * -f: path to new property file (*not yet implemented!*)
  * -t: yes or 1 - use to produce plain text output
  * -n: path to text file with list of tasks to be used instead of JIRA server

### Output
XML file compatible with MS proj and OpenProj

### Dependencies
- jira
- lxml
- urllib3

### References

 - https://stackoverflow.com/questions/2415943/what-is-the-xml-spec-for-importing-into-microsoft-project
 - https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2007/bb968733(v=office.12)
