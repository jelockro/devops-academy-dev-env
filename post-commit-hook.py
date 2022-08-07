# place in .git/hooks/post-commit
import sys,subprocess,re
print ("checking for version change...")

status, output = subprocess.getstatusoutput('git diff HEAD HEAD^ -U0')

version_info = None

for d in output.split("\n"):
    rg = re.compile("## (?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<revision>[0-9]+)")
    m  = rg.search(d)
    if m:
       version_info = m.groupdict()
       break

if version_info:
    tag = "%s.%s.%s" % (version_info['major'], version_info['minor'], version_info['revision'])
    status, output = subprocess.getstatusoutput('git tag -f %s' % tag)
    if status:
       raise Exception('tagging not successful: %s %s' % (output, status))
    print ("tagged revision: %s" % tag )
else:
    print ( "none found.")
