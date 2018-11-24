def parse_raw_choices(str):
    """
    Parses choices from a raw text string, so it's possible to do things like this:

    MYFIELD_CHOICES=parse_raw_choices(
        '''
        # Comments (prefixed with "#"), empty lines and spacing are supported
        # (whitespace improves readability)

        This option number one          [option_one]
        This is option two              [option_two]

        Aaand option 3                  [option_three]
        '''
    )

    """
    choices = []
    lines = str.strip().split('\n')
    for line in lines:
        if line and not line.startswith('#'): # skip empty lines and comments
            line = line.strip()
            if line.endswith(']'):
                cutoff = line.rfind('[')
                if cutoff != -1:
                    x = line[cutoff+1:-1].strip()
                    y = line[:cutoff-1].strip()
                    if x == 'None': # treat None literally as a null value
                        x = None
                    choices.append(tuple([x,y]))
    return tuple(choices)

def get_longest_key(tuple_of_tuples):
    """
    Why is this needed? Because sometimes we want to know how long a CharField
    should be -- so let's have it as long as the longest choice available.
    (For example, when we have a radio button and we want to store a single value.)

    INPUT=(
        ('short', 'blahblahblah'),
        ('longer', 'blahblahblah'),
        ('longest', 'blahblahblah')
    )
    OUTPUT=len(longest)

    USAGE:
    BLAH_CHOICES=(...)
    blah=CharField(max_length=get_longest_key(BLAH_CHOICES))
    """
    return max(len(i) for i in dict(tuple_of_tuples).values())
