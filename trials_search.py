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
            added_trial_counter = 0
            repeated_counter = 0
            failed_to_read_counter = 0
            ff.readline() #skips the title line
            line_read_counter = 0
            while True:
                line_read_counter += 1
                try:
                    line=ff.readline()
                except:
                    failed_to_read_counter += 1
                    continue
                #breaks at last line
                if not line:
                    break
                else:
                    #splits by tabs
                    try:
                        fields = line.split("\t")
                        rank = int(fields[0])
                    except:
                        continue
                    # instances a new trial for each line and includes in list of trials
                    trial=(Trial(fields[0], fields[1], fields[2], fields[3], fields[4],fields[5], fields[6], fields[7], file))
                    if not trial.repeated(trials):
                        trials.append(trial)
                        added_trial_counter += 1
                    else:
                        repeated_counter += 1
            print('The last record imported in file {} was rank {}. Excluding {} repeated '
                  'imported {} trials. \n Lines read {} and failed to read {} lines'.format(file,
                    fields[0], repeated_counter, added_trial_counter, line_read_counter, failed_to_read_counter))
    return trials

class Word_list(object):
    word_list = set()
    word_dict = {}
    print('iniciei wordlist class')

    def __init__(self, title, conditions, interventions, trial_id):
        self.words=[]
        self.title=title
        self.conditions=conditions
        self.interventions=interventions
        self.trial_id=trial_id
        self.Add_words()

    def Add_words(self):
        self.words = self.title.split(" ") + self.conditions.split(" ") + self.interventions.split(" ")
        Word_list.word_list=Word_list.word_list.union(set(self.words))
        for word in self.words:
            if word in Word_list.word_dict.keys():
                Word_list.word_dict[word].append(self.trial_id)
            else:
                Word_list.word_dict[word]=[self.trial_id]
        return self.words

class Trial(object):
    """
    Class that holds an instance for each trial
    """
    id_counter=0
    def __init__(self, rank, title, status, study_results, conditions, interventions, locations, url, file_name):
        Trial.id_counter += 1
        self.id=Trial.id_counter
        self.rank=rank
        self.title=title
        self.status=status
        self.study_results=study_results
        self.conditions=conditions
        self.interventions=interventions
        self.locations=locations
        self.url=url
        self.file_name = file_name
        self.key_words = Word_list (title, conditions, interventions, self.id)

    def repeated(self, trials):
        for trial in trials:
            if trial.title == self.title:
                return True
        return False


if __name__ == '__main__':

    # laods trials asking the user for file names and starts trials from an empty list
    files=['210618_lymphoma_tcell.tsv','210618_leukemia_lymphoblastic.tsv']
    trials=Load_trials(files)
    print(trials)
    print (Word_list.word_dict)

