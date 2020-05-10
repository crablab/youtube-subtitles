class dumb_analyzer:
    """
    A naive and inefficient moving variable window length phrase frequency analyser. 
    """

    def __init__(self, window_min=1, window_max=5, window_increment=1):
        self._min = window_min
        self._max = window_max
        self._increment = window_increment
    
    def most_frequent_phrases(self, string, limit=5):
        """
        Works out the most frequent phrases in the string. 

        :param string: The string to analyse.
        :param limit: Number of results to return (default = 5)
        """

        # Calculate the frequent phrases
        frequencies = self._get_frequencies(string)

        return self._sort_frequencies(frequencies, limit)

    def _get_frequencies(self, string):
        # Check the string is at least the current window max 
        if(len(string) < self._max):
            raise Exception("String is shorter than the window size!")

        # Calculate length and split into words  
        string = string.split()
        length = len(string)
        frequencies = {}

        for index, word in enumerate(string):
            eow_flag = 0

            for current_window_size in range(0, self._max, self._increment):
                # Check our window isn't off the end of the array
                upper_bound = current_window_size + index + 1

                if(upper_bound < length + 1):
                    phrase = " ".join(string[index:upper_bound])

                    if(phrase in frequencies):
                        frequencies[phrase] += 1
                    else:
                        frequencies[phrase] = 1
                else:
                    eow_flag = 1
                    continue

            if(eow_flag):
                eow_flag = 0
                continue
        
        return frequencies

    def _sort_frequencies(self, frequencies, limit, lower_word_limit=2):
        limited = []
        counter = 0 

        for key, value in enumerate(sorted(frequencies.items(), key=lambda x: x[1], reverse=True)):
            if(counter < limit):
                # Check for singleton 
                if(len(value[0].split()) > lower_word_limit):
                    limited.append(value)
                    counter += 1
                else:
                    continue
            else:
                break
        
        return limited
