import re
import time
import datetime as dt


def msg(s, level=0):
    plug = 'cuda_plain_tasks'
    if level == 0:
        print('{}: {}'.format(plug, s))
    elif level == 1:
        print('{} WARNING: {}'.format(plug, s))
    elif level == 2:
        print('{} ERROR: {}'.format(plug, s))


def get_indent(line):
    space = ' \t'
    for n, l in enumerate(line):
        if l not in space:
            return n
    else:
        return len(line)


def get_word_under_cursor(line, x, seps='.,:-!<>()[]{}\'"\t\n\r'):
    """
    get current word under cursor position
        line str: line of text
        x int: position cursor in line(0-based)
        [seps] str: chars as separators for words
        return (word, (start, end, local position cursor in word))
        """
    if not 0 <= x <= len(line):
        return
    if seps:
        ln = list(line)
        for n, char in enumerate(ln):
            if char in seps:
                ln[n] = ' '
        s = ''.join(ln)
    else:
        s = line
    start = max(s.rfind(' ', 0, x)+1, 0)
    end = s.find(' ', x)
    end = len(line) if end == -1 else end
    word = line[start:end]
    return (word, (start, end, max(x-start, 0)))


class Parser:
    def __init__(self):
        self.re_header = re.compile(r'^\s*(\w+.*?):\s*$')
        self.re_separator = re.compile(r'^\s*---.{3,5}---+$')
        self.re_item_bullet_open = re.compile(r'^\s*(\-|❍|❑|■|□|☐|▪|▫|–|—|≡|→|›|\[\s\]|\[\])')
        self.re_item_bullet_done = re.compile(r'^\s*(\+|✓|✔|☑|√|\[x\]|\[\+\])')
        self.re_item_bullet_cancel = re.compile(r'^\s*(x|✘|\[\-\])')
        self.re_tag_done = re.compile(r'\s*@done(\([\w,\.:\-\/ @]*\))?')
        self.re_tag_cancel = re.compile(r'\s*@cancelled(\([\w,\.:\-\/ @]*\))?')
        self.re_tag_lasted = re.compile(r'\s*@lasted(\([\w,\.:\-\/ @]*\))?')
        self.re_tag_wasted = re.compile(r'\s*@wasted(\([\w,\.:\-\/ @]*\))?')
        self.re_tag_created = re.compile(r'\s*@created(\([\w,\.:\-\/ @]*\))?')
        self.re_tag_started = re.compile(r'\s*@started(\([\w,\.:\-\/ @]*\))?')
        self.re_tag_toggle = re.compile(r'\s*@toggle(\([\w,\.:\-\/ @]*\))?')
        self.re_start_space = re.compile(r'^\s*')

    @staticmethod
    def getbool(val):
        return bool(val)

    def isheader(self, line):
        r = self.getbool(self.re_header.match(line))
        return r

    def isseparator(self, line):
        r = self.getbool(self.re_separator.match(line))
        return r

    def isitemopen(self, line):
        r = self.getbool(self.re_item_bullet_open.match(line))
        return r

    def isitemdone(self, line):
        r = self.getbool(self.re_item_bullet_done.match(line))
        return r

    def isitemcancel(self, line):
        r = self.getbool(self.re_item_bullet_cancel.match(line))
        return r

    def isitem(self, line):
        return any([self.isitemopen(line),
                    self.isitemdone(line),
                    self.isitemcancel(line)])

    def issimpletext(self, line):
        return not any([self.isheader(line),
                        self.isitem(line),
                        self.isseparator(line)
                        ])

    @staticmethod
    def getgroup(res, n=0):
        try:
            return res.group(n)
        except Exception:
            return ''

    def get_tag_done(self, line):
        return self.getgroup(self.re_tag_done.search(line), 0)

    def del_tag_done(self, line):
        return self.re_tag_done.sub('', line)

    def get_tag_cancel(self, line):
        return self.getgroup(self.re_tag_cancel.search(line), 0)

    def del_tag_cancel(self, line):
        return self.re_tag_cancel.sub('', line)

    def has_tag_lasted(self, line):
        return self.getbool(self.re_tag_lasted.search(line))

    def del_tag_lasted(self, line):
        return self.re_tag_lasted.sub('', line)

    def has_tag_wasted(self, line):
        return self.getbool(self.re_tag_wasted.search(line))

    def del_tag_wasted(self, line):
        return self.re_tag_wasted.sub('', line)

    def has_tag_created(self, line):
        return self.getbool(self.re_tag_created.search(line))

    def get_tag_created_date(self, line):
        return self.getgroup(self.re_tag_created.search(line), 1)

    def has_tag_started(self, line):
        return self.getbool(self.re_tag_started.search(line))

    def get_tag_started_date(self, line):
        return self.getgroup(self.re_tag_started.search(line), 1)

    def get_tag_toggle_dates(self, line):
        return self.re_tag_toggle.findall(line)

    def get_start_space(self, line):
        return self.getgroup(self.re_start_space.match(line), 0)

    def get_header(self, line):
        return self.getgroup(self.re_header.match(line), 1)


class Date:

    def __init__(self):
        pass

    def datenow(self, date_format):
        return self.tznow().strftime(date_format)

    @staticmethod
    def tznow():
        t = time.time()
        d = dt.datetime.fromtimestamp(t)
        u = dt.datetime.utcfromtimestamp(t)
        return d.replace(tzinfo=dt.timezone(d - u))

    def calculate_time_for_task(self, started, togles, date_format):
        if not started:
            return

        try:
            start = dt.datetime.strptime(started, date_format)
            end = dt.datetime.strptime(self.datenow(date_format), date_format)

            toggle_times = [dt.datetime.strptime(toggle, date_format) for toggle in togles]
            all_times = [start] + toggle_times + [end]
            pairs = zip(all_times[::2], all_times[1::2])
            deltas = [pair[1] - pair[0] for pair in pairs]

            return self.format_delta(sum(deltas, dt.timedelta()))
        except ValueError as ex:
            msg(ex, 2)

    @staticmethod
    def format_delta(delta):
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        res = []
        if days > 1:
            res.append('{}days'.format(days))
        elif days == 1:
            res.append('1day')
        if hours > 0:
            zero = '0' if minutes < 10 else ''
            res.append('{}:{}{}'.format(hours, zero, minutes))
        else:
            res.append('{}min'.format(minutes))
        return '(' + ' '.join(res) + ')'
