'''
This file is part of soco.
'''

def find_max(list=[[2,7,4], [43,3,-2]], col=2):
    maxrecord = list[0]
    for record in list:
        #print(record)
        if record[col] > maxrecord[col]:
            maxrecord = record
    return maxrecord[col], maxrecord

def find_min(list=[[2,7,4], [43,3,-2]], col=2):
    minrecord = list[0]
    for record in list:
        #print(record)
        if record[col] < minrecord[col]:
            minrecord = record
    return minrecord[col], minrecord

def find_maxabs(list=[[2,7,4], [43,3,-32]], col=2):
    maxabsrecord = list[0]
    for record in list:
        #print(record)
        if abs(record[col]) > abs(maxabsrecord[col]):
            maxabsrecord = record
    return abs(maxabsrecord[col]), maxabsrecord

def describe_ranges(values, range_word="TO", sep=" "):
    """
    Convert a list of integers into a compact range description string.

    Examples:
        [1,2,3,4,8,11,12,13] -> "1 TO 4 8 11 TO 13"
        [5]                  -> "5"
        []                   -> ""
        [-3, -2, -1, 0, 2]   -> "-3 TO 0 2"

    Parameters
    ----------
    values : Iterable[int]
        The input numbers (will be de-duplicated and sorted).
    range_word : str, optional
        The token used to denote ranges. Default is "TO".
    sep : str, optional
        Separator between parts. Default is a single space.

    Returns
    -------
    str
        The compact range description.
    """
    # Normalize: sort unique integers
    nums = sorted(set(int(v) for v in values))
    if not nums:
        return ""

    parts = []
    start = prev = nums[0]

    def emit_range(a, b):
        if a == b:
            parts.append(str(a))
        else:
            parts.append(f"{a} {range_word} {b}")

    for n in nums[1:]:
        if n == prev + 1:
            # still in a run
            prev = n
        else:
            # end current run
            emit_range(start, prev)
            # start new run
            start = prev = n
    # emit last run
    emit_range(start, prev)

    return sep.join(parts)


#test if main
if __name__ == '__main__':
    pass