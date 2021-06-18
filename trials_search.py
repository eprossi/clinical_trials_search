"""

"""

def Add_file(files):
    file = str(input('input file name when done press enter'))
    if file:
        files.append(file)
        return files
    return

def Load_trials(files=[], trials=[]):
    """
    Takes in files (list of strings with names of the files to load)
    Takes in a trials list (of previously instanced trials)
    if it empty, it will request user to input each file
    if trials empty it will start from scratch
    Reads files and instances one Trial for each trial
    the files must have 7 text fields in the order
    title, status, study_results, conditions, interventions, locations, url
    where the first line is a titles line that gets ignored.
    Returns list trials with references to each trial instanced
    """

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
                trials.append(Trial(fields[0], fields[1], fields[2], fields[3], fields[4],fields[5], fields[6], file))
    return trials

class Trial(object):
    """
    Class that holds an instance for each trial
    """
    id_counter=0
    def __init__(self, title, status, study_results, conditions, interventions, locations, url, file_name):
        Trial.id_counter += 1
        self.id=Trial.id_counter
        self.title=title
        self.status=status
        self.study_results=study_results
        self.conditions=conditions
        self.interventions=interventions
        self.locations=locations
        self.url=url
        self.file_name = file_name


if __name__ == '__main__':
    # laods trials asking the user for file names and starts trials from an empty list
    Load_trials()

