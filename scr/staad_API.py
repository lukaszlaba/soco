import os
import re

from openstaad import Geometry, Root, Output, Load


_force_units = {}
_force_units['[kN]'] = 1.0
_force_units['[kip]'] = 4.4482216

_moment_units = {}
_moment_units['[kN-m]'] = 1.0
_moment_units['[kip-ft]'] = 1.3558179
_moment_units['[kip-in]'] = 0.1129848


def get_available_force_units():
    return list(_force_units)


def get_available_moment_units():
    return list(_moment_units)

def instance_exist():
    try:
        filename = Root().GetSTAADFile()
        if filename: return True
        else: return False
    except:
        return False


def get_selected_members():
    if not instance_exist(): return []
    return list(Geometry().GetSelectedBeams())


def get_selected_nodes():
    if not instance_exist(): return []
    return list(Geometry().GetSelectedNodes())


def get_filename():
    if not instance_exist(): return ''
    filename = Root().GetSTAADFile()
    filename = os.path.basename(filename)
    return filename

def staad_force_unit():
    if not instance_exist(): return ''
    base_unit = Root().GetBaseUnit()
    if base_unit == 'Metric':
        return '[kN]'
    if base_unit == 'English':
        return '[kip]'


def staad_moment_unit():
    if not instance_exist(): return ''
    base_unit = Root().GetBaseUnit()
    if base_unit == 'Metric':
        return '[kN-m]'
    if base_unit == 'English':
        return '[kip-in]'


def get_beam_end_forces_tabe(lc_list=[1, 2, 3], force_unit='[kip]', moment_unit='[kip-in]', progress_bar=None):
    """
    Collect beam end forces for selected beams (or all beams) across specified load cases.

    Returns a list of rows:
        [member, lc, Node, Fx, Fy, Fz, Mx, My, Mz]

    Notes on units:
    - Staad return: for 'Metric' BaseUnit kN, kNm | for 'English' BaseUnit kip, kip-in
    - Assumes Output.GetMemberEndForces returns [Fx, Fy, Fz, Mx, My, Mz] in the model's internal force/moment BaseUnit.
    - If the inended moment unit label is '[kip-ft]', this function divides the returned moments by 12
      (i.e., assumes the API returns kip-in internally and we want kip-ft as final output).
    """
    if not instance_exist(): return []
    #--
    _staad_force_unit = staad_force_unit()
    _staad_moment_unit = staad_moment_unit()
    #--
    geometry = Geometry()
    load = Load()
    output= Output()
    #--
    mlist = geometry.GetSelectedBeams()
    if not mlist:
        mlist = geometry.GetBeamList()
    #--
    if progress_bar:
        progress_bar.setVisible(True)
        progress_bar.setValue(0)
    #--
    def convert_forces(values):
        force_factor = _force_units[_staad_force_unit] / _force_units[force_unit]
        for i in range(0, 3):
            values[i] = values[i] * force_factor
        moment_factor = _moment_units[_staad_moment_unit] / _moment_units[moment_unit]
        for i in range(3, 6):
            values[i] = values[i] * moment_factor
        #print(force_factor, moment_factor)

    #--
    out_table = []
    progress_counter = 0
    for m in mlist:
        mrec = m
        m_points = geometry.GetMemberIncidence(m)
        for l in lc_list:
            #member start
            values = list(output.GetMemberEndForces(beam=m,start=True,lc=l))
            #value format - [Fx, Fy, Fz, Mx, My, Mz]
            convert_forces(values)
            values = list(map(lambda x: round(x, 3), values))
            start_res = [str(mrec), str(l), str(m_points[0])] + values
            #res format - [member, lc, Node, Fx, Fy, Fz, Mx, My, Mz]
            out_table.append(start_res)
            #-
            mrec = ''
            #member end
            values = list(output.GetMemberEndForces(beam=m,start=False,lc=l))
            convert_forces(values)
            values = list(map(lambda x: round(x, 3), values))
            end_res = [str(mrec), str(l), str(m_points[1])] + values
            out_table.append(end_res)
        #--
        if progress_bar:
            progress_counter += 1
            progress_bar.setValue(int(progress_counter/len(mlist)*100))
        #--
    #--
    if progress_bar:
        progress_bar.setVisible(False)
        progress_bar.setValue(0)
    #--
    return out_table


def get_lc_list_for_envelope(envelope='1 TO 10 13'):
    if not instance_exist(): return []
    #--
    all_lc = Load().GetPrimaryLoadCaseNumbers()
    out_lc_list = [i for i in all_lc if _in_specified_ranges(i, envelope)]
    return out_lc_list


def _in_specified_ranges(x, spec): #AI generated
    """
    Return True if number x belongs to the ranges described by `spec`.

    spec examples:
        "2000 2145 TO 2164 4000 TO 4071"
        "100, 105 TO 110, 200"
        "-10 TO -5 0 5 TO 7"
    """
    # Normalize: remove commas, collapse whitespace, uppercase for "TO"
    tokens = re.split(r"\s+", spec.replace(",", " ").strip().upper())
    i = 0
    while i < len(tokens):
        t = tokens[i]

        # Try to read a single integer token
        def is_int(s):
            return re.fullmatch(r"[+-]?\d+", s) is not None

        if is_int(t):
            a = int(t)
            # Check if this is a range: "<a> TO <b>"
            if i + 2 < len(tokens) and tokens[i + 1] == "TO" and is_int(tokens[i + 2]):
                b = int(tokens[i + 2])
                lo, hi = (a, b) if a <= b else (b, a)
                if lo <= x <= hi:
                    return True
                i += 3
            else:
                # Single value
                if x == a:
                    return True
                i += 1
        else:
            # Skip anything unexpected (e.g., stray words)
            i += 1
    return False


def describe_ranges(values, range_word="TO", sep=" "): #AI generated
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


def extract_envelope_ranges_by_id(std_path): #AI generated
    """
    Parse a STAAD .std file for lines of the form:
        "<segments> ENVELOPE <id> [TYPE <type>]"
    where <segments> is a space-separated sequence of:
        - single integers, e.g., "2000"
        - ranges "A TO B", e.g., "2145 TO 2164"
    Examples:
        "2000 TO 2164 ENVELOPE 3 TYPE STRENGTH"
        "2000 2145 TO 2164 4000 TO 4071 ENVELOPE 5"

    Returns a dict keyed by envelope ID:
        { <id>: "<normalized segments>" }
    If the same id appears multiple times, segments are appended with a space.
    Comment lines starting with '*' and empty lines are ignored.
    """

    # Split the line into <prefix> ENVELOPE <id> [TYPE <type>]
    env_split_re = re.compile(
        r'^(?P<prefix>.+?)\s+ENVELOPE\s+(?P<id>\d+)(?:\s+TYPE\s+\S+)?\s*$',
        flags=re.IGNORECASE
    )

    def normalize_prefix(prefix: str) -> str:
        """
        Normalize the <prefix> so it contains only integers and 'TO',
        with single spaces and uppercase 'TO'. Also accepts compact
        tokens like '2145TO2164' and splits them correctly.
        """
        s = prefix.upper().strip()
        s = re.sub(r'\s+', ' ', s)
        tokens = []
        for tok in s.split(' '):
            if not tok:
                continue
            if tok == 'TO':
                tokens.append('TO')
            elif re.fullmatch(r'\d+', tok):
                tokens.append(str(int(tok)))  # normalize leading zeros
            else:
                # Recover cases like "2145TO2164"
                m = re.fullmatch(r'(\d+)TO(\d+)', tok)
                if m:
                    tokens.extend([str(int(m.group(1))), 'TO', str(int(m.group(2)))])
                else:
                    # Unexpected token; raise to skip this line gracefully
                    raise ValueError(f"Unexpected token: {tok}")
        return ' '.join(tokens)

    result: Dict[int, str] = {}

    with open(std_path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('*'):
                continue

            m = env_split_re.match(line)
            if not m:
                continue

            prefix = m.group('prefix')
            try:
                range_str = normalize_prefix(prefix)
            except ValueError:
                # Skip malformed prefixes
                continue

            env_id = int(m.group('id'))

            if env_id in result and result[env_id]:
                # Append segments for repeated IDs
                result[env_id] = f"{result[env_id]} {range_str}"
            else:
                result[env_id] = range_str

    return result

#test if main
if __name__ == '__main__':
    pass
    #print(instance_exist())
    #print(get_selected_members())
    #print(get_selected_nodes())
    for i in get_beam_end_forces_tabe():
        print(i)