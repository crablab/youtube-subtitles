class subtitle:
    """
    Digests a YouTube subtitle file.
    """

    def __init__(self, file):
        try: 
            f = open(file, "r")
            self._file = f
        except IOError:
            raise Exception("Cannot open subtitle file.")
    
    def get_all_text(self):
        """
        Parses the file into a single string.

        :returns: String with entire subtitle transcript 
        """
        
        text = ""

        for number, line in enumerate(self._file, 1):
            if(number == 2 or ((number - 2) % 3) == 0):
                text = text + " " + line
        
        return text