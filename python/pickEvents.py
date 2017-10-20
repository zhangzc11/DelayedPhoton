from subprocess import call, check_output
import csv

def matches(dataset):
    """Returns true if we should use this dataset"""
    required = ['RAW','DoubleEG']#,'18Apr2017']
    for r in required:
        if r not in dataset:
            return False
    return True

with open("events.txt", 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=' ')
    for row in reader:
        run, lumi, event = filter(None, row)
        event_string = "%s:%s:%s"%(run, lumi, event)
        print event_string

        # DAS query to find dataset name
        query = "'dataset run=%s'"%(run)
        cmd = 'das_client --query='+query+' --limit=0'
        print cmd
        output = check_output(cmd, shell=True)
        filtered = filter(matches, output.split('\n'))
        if len(filtered) == 0:
            print "No matches found!"
            continue
        dataset = filtered[0]

        # Find events
        pick_cmd = "edmPickEvents.py '%s' %s"%(dataset, event_string)
        print pick_cmd
        copy_cmd = check_output(pick_cmd, shell=True)
        copy_cmd = copy_cmd.replace("pickevents.root",
                "pickevents%s.root"%(event_string.replace(":","_")))

        # Get ROOT file
        print copy_cmd
        call(copy_cmd, shell=True)
