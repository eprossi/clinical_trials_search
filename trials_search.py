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
        with open(file) as ff:
            added_trial_counter = 0
            repeated_counter = 0
            failed_to_read_counter = 0
            ff.readline()  # skips the title line
            line_read_counter = 0
            while True:
                line_read_counter += 1
                try:
                    line = ff.readline()
                except:
                    failed_to_read_counter += 1
                    continue
                # breaks at last line
                if not line:
                    break
                else:
                    # splits by tabs
                    try:
                        fields = line.split("\t")
                        rank = int(fields[0])
                    except:
                        continue
                    # instances a new trial for each line and includes in list of trials
                    trial = (
                        Trial(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7],
                              file))
                    if not trial.repeated(trials):
                        trials.append(trial)
                        added_trial_counter += 1
                    else:
                        repeated_counter += 1
            print('The last record imported in file {} was rank {}. Excluding {} repeated '
                  'imported {} trials. \n Lines read {} and failed to read {} lines'.format(file,
                                                                                            fields[0], repeated_counter,
                                                                                            added_trial_counter,
                                                                                            line_read_counter,
                                                                                            failed_to_read_counter))
    return trials

class Word(object):
    word_counter = 0
    # slots limita os atributos de cada instance do objeto. Fica mais rapido. mas menos flexivel.
    __slots__ = ('word', 'frequency', 'trials', 'id')

    def __init__(self, word, trial_id):
        self.word = word
        self.frequency = 1
        self.trials = {trial_id}
        self.id = Word.word_counter
        Word.word_counter += 1

    def add(self, trial_id):
        self.frequency += 1
        self.trials.add(trial_id)

class Word_list(object):
    def __init__(self):
        self.word_list = []

    def union(self, title, conditions, interventions):
        word_union = title.split(";' |,") + conditions.split(";' |,") + interventions.split(";' |,")
        return word_union

    def add_words(self, words, trial_id):
        for word in words:
            found_word = False
            for instance in self.word_list:
                if instance.word == word:
                    instance.add(trial_id)
                    found_word = True
                    break
            if not found_word:
                self.word_list.append(Word(word, trial_id))

    def get(self):
        return self.word_list

class Trial():
    """
    Class that holds an instance for each trial
    """
    id_counter = 0

    def __init__(self, rank, title, status, study_results, conditions, interventions, locations, url, file_name):
        Trial.id_counter += 1
        self.id = Trial.id_counter
        self.rank = rank
        self.title = title
        self.status = status
        self.study_results = study_results
        self.conditions = conditions
        self.interventions = interventions
        self.locations = locations
        self.url = url
        self.file_name = file_name
        self.create_word_list()

    def create_word_list(self):
        wlist=Word_list()
        all_words = wlist.union(self.title, self.conditions, self.interventions)
        wlist.add_words(all_words, self.id)


    def repeated(self, trials):
        for trial in trials:
            if trial.title == self.title:
                return True
        return False


if __name__ == '__main__':
    #initializes Word_list
    wl=Word_list()

    # laods trials asking the user for file names and starts trials from an empty list
    files = ['210618_lymphoma_tcell.tsv', '210618_leukemia_lymphoblastic.tsv']

    trials = Load_trials(files)

    print(trials)

    print(wl.get())
    print ('word counter: {}'. format(Word.word_counter))
    print(f'word counter: {Word.word_counter}')
    print('word counter: \n', Word.word_counter)
