"""
starting fresh the search engine with objects

OBJECTIVE:
Word claud with the most FREQUENT WORDS
when WORD tagged with YES/NO/IGNORE - select TRIALS that have / do not have that WORRD
and then do a new WORD CLOUD only with the SELECTED TRIALS

each trial shall has the fiels from CLINICAL TRIALS FILES

when a new TRIAL is added, it
scouts for the WORDS and instances in WORD class if not yet present
each WORD has its FREQUENCY, the TRIALS that have that word
then just using WORD, I can create the CLOUD. by testing the attributes

MAYBE use a SUPERCLASS (or a CLASS ATTRIBUTE) - with the list of words and the YES/NO/IGNORE
or use YES/NO/IGNORE in the instance of WORD itself. ??
I am liking a class attribute with the list of words - remember to initiate the class?

WORDCLOUD - should be a CLASS with list of YES WORDS and FREQUENCIES and DECISION ATTRIBUTES (YES, NO, IGNORE) and
set of TRIALS in that WORDCLOUD


class structure:
each trial has many words
each word has many trials
each word is its own unique counter_id
each trial has an unique counter_id

each CLOUD has it's cloud ID and selection criteria
I should be able to print all available clouds - id, and criteria

TRIAL CLASS
- list of trials (sorted by unique_ID and Description and INSTANCE)
- class method - setter trial - checks if repeated and add if not. Adds to list of trials. Adds 1 to counter.
- class method - getter trial - by ID (s) returns a list of the  the specific trial (s)
- class attribute - trial counter: setter trial adds 1 every time there is no repeated
TRIAL INSTANCES
- instanced by the class method
- attributes: unique_id, fiels from clinicaltrials.org
- when init - runs WORD class method sending list of words, trial ID.


WORD CLASS - MAYBE NOT NEEDED..... #
- class attribute - list of words with ID,word, and INSTANCE
- class method - receives list of words and trial ID - checks IF exists - if so add FREQUENCY and trial ID
WORD INSTANCES
- instanced ty the class method
- attributes: unique_id, word,ignore, frequency, trial_id list
- word setter - to set ignore in particular words


CLOUD
attributes: ID, parent, word, yes or no, list of trials [], list of words/yes/no, words and frequency, ignore_words
method new_cloud - run a series of methods:
                   gets trials from parent, filters with new word and set new list of trials
                   gets parents yes words and no words and updates
                   get new list of trials and gets all the words that have them if
                                     either all trials have a list of words in them (then search by trials)
                                     or i have to go word by word and match trials
                                     i think that better for trials to have the words list because  less trials
                                     than words.
                                     do words need to have trials?  maybe not.




when i select a word, it needs to find all trials that have that word and then select all words that are in that list
of trials.
each word has a number of trials.
when i say yes to that word, i need to take the list of trials of that word
then i say yes to another word - I REMOVE all trials from the first list that ARE NOT in the second words list
then i say NO to a word - I take the list of the TRIALS of that word and REMOVE from the trial list.
AT THE END I get this new list of trials and get all their words AND NEW FREQUENCY
This all needs to happen in the CLOUD class


"""


class Trial(object):
    """
    Class that holds an instance for each trial
    """
    id_counter = 0
    trials = [] ##MUDEI DE IDEIA - LISTA SO DAS INSTANCES... # dict of trials (sorted by unique_ID and TITLE and INSTANCE)

    @classmethod
    def get_trials(cls, trial_ids):
        """
        takes ids of the trials being searched
        returns a list of such trials
        """
        trials = [Trial.trials[id].instance for id in trial_ids]
        return trials

    @classmethod
    def repeated (cls, new_trial_title):
        for trial in Trial.trials:
            if new_trial_title == trial.title:
                return True
        return False

    @classmethod
    def add_trial(cls, rank, title, status, study_results, conditions, interventions, locations, url, file_name):
        """
        takes in all the fields from the importaed line
        if not repeated instances and adds to list of Trials
        """
        if not repeated(title):
            Trial.id_counter += 1
            Trial.trials.append(Trial(Trial.id_counter, rank, title, status, study_results, conditions,
                                      interventions, locations, url, file_name))

    @classmethod
    def all_trials_getter (cls):
        returns (cls.trials.copy())

    def __init__(self, id, rank, title, status, study_results, conditions, interventions, locations, url, file_name):
        self.id = id
        self.rank = rank
        self.title = title
        self.status = status
        self.study_results = study_results
        self.conditions = conditions
        self.interventions = interventions
        self.locations = locations
        self.url = url
        self.file_name = file_name
        self.words = self.create_word_list ()

    def split(self, string):
        """splits strings and return list of words"""
        return (string.split(";' |,"))

    def create_word_list(self):
        """creates its own word set """
        return set(split(self.title)+split(self.conditions)+split(self.interventions))

class Cloud (object):
    """
    each cloud instance has a parent, a word that it adds or removes, a list of ignores, list of words and frequencies
    """
    id_counter = 0

    def __init__(self, word, yes_no, ignore=[], parent = None):
        Cloud.id_counter += 1
        self.id = Cloud.id_counter
        self.word = word
        self.yes_no=yes_no
        self.ignore = ignore
        self.parent=parent

        self.trials_in_cloud = []
        self.yes_words = set()
        self.no_words = set()
        self.ignore_words = set()
        self.word_frequency_dict = {}

    def filter_trials(self, parent_trials, new_word, yes_no):
        # takes old trials, loops them selecting only the yes or removing the nos / returns list
        if yes_no == 'y' or yes_no == 'yes':
        raise exception NotImplemented


    def get_parent_data (self, parent):
        """
        takes in parent
        returns a tupple with sets of parent trials, yes, no, ignore
         if parent is NONE (first instance) - returns a tupple of all trials + 3 empty sets
        """
        try:
            return (parent.trials_in_cloud.copy(), parent.yes_words.copy(), parent.no_words.copy(), parent.ignore_words.copy())
        except:
            return (Trials.all_trial_getter(), {}, {}, {})

    def updates_sets(self, parent_yes, parent_no, parent_ignore):
        """
        updates yes, no and ignore sets, including the parents, the self word
        it includes "union" of yes, no and ignore - even though self starts with empty sets
        I left it here because in the future maybe I include something new that makes these sets
        not empty before bringing the parent info.
        """
        self.yes_words = set.union(self.yes_words, parent_yes) # this seems redundant
        self.no_words = set.union(self.no_words, parent_no) # this seems redundant
        self.ignore_words = set.union(self.ignore_words, parent_ignore, self.ignore) # this seems redundant
        if self.yes_no == 'y' or self.yes_no == 'yes':
            self.yes_words.add(self.word)
        elif self.yes_no == 'n' or self.yes_no == 'no':
            self.no_words.add(self.word)

    def create_cloud_dict (self, trials_in_cloud):
        """
        gets trials in cloud
        loops every filtered trial and adds word + frequeny to dict
        returns dictionary
        """
        dict = {}
        for trial in trials_in_cloud:
            for word in trial.words:
                if word in dict:
                    dict[word] += 1
                else:
                    dict[word] = 1
        return dict

    def new_cloud (self):
        # gets trials, yes, no and ignore from parent
        self.parent_trials, self.parent_yes, self.parent_no, self.parent_ignore = get_parent_data (parent)
        #updates sets (yes, no and ignore) of self by adding parent info
        self.updates_sets(self.parent_yes, self.parent_no, self.parent_ignore)
        self.trials_in_cloud = self.filter_trials(self.parent_trials, self.word, self.yes_no)
        self.word_frequency_dict = self.create_cloud_dict (self.trials_in_cloud)

"""
method new_cloud - run a series of methods:
 done                  gets trials from parent, filters with new word and set new list of trials
 done                  gets parents yes words and no words and updates
                   get new list of trials and gets all the words that have them if
                                     either all trials have a list of words in them (then search by trials)
                                     or i have to go word by word and match trials
                                     i think that better for trials to have the words list because  less trials
                                     than words.
                                     do words need to have trials?  maybe not.




when i select a word, it needs to find all trials that have that word and then select all words that are in that list
of trials.
each word has a number of trials.
when i say yes to that word, i need to take the list of trials of that word
then i say yes to another word - I REMOVE all trials from the first list that ARE NOT in the second words list
then i say NO to a word - I take the list of the TRIALS of that word and REMOVE from the trial list.
AT THE END I get this new list of trials and get all their words AND NEW FREQUENCY
This all needs to happen in the CLOUD class
