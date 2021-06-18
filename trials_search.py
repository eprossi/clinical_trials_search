"""

"""

def Add_file(files):
    file = str(input('input file name when done press enter'))
    if file:
        files.append(file)
        return files
    return

def Load_trials():
    files=[]

    # adds each file to files list
    while True:
        if not Add_file(files):
            break

    for file in files:
        with open (file) as ff:
            line_counter = 0
            while True:
                line=ff.readline()
                #breaks at last line
                if not line:
                    break
                #skip the first line that has field names
                elif line_counter==0:
                    continue
                line_counter += 1
                #splits by tabs
                fields=line.split("\t")
                # instances a new trial for each line and includes in list of trials
                trials.append(Trial(fields[0], fields[1], fields[2], fields[3], fields[4],fields[5], fields[6]))

class Trial(object):
    id_counter=0
    def __init__(self, title, status, study_results, conditions, interventions, locations, url):
        self.title=title
        self.status=status
        self.study_results=study_results
        self.conditions=conditions
        self.interventions=interventions
        self.locations=locations
        self.url=url
        Trial.id_counter += 1
        self.id=Trial.id_counter


if __name__ == '__main__':
    trials=[]
    Load_trials()