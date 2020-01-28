import os
import re
import json
import cudatext as ct
import cuda_options_editor as op_ed

fn_config = 'cuda_plain_tasks.json'
config_file = os.path.join(ct.app_path(ct.APP_DIR_SETTINGS),
                           fn_config)


def _json_load(s, *args, **kwargs):
    ''' Adapt s for json.loads
            Delete comments
            Delete unnecessary ',' from {,***,} and [,***,]
    '''

    def rm_cm(match):
        line = match.group(0)
        pos = 0
        in_str = False
        while pos < len(line):
            ch = line[pos]
            if ch == '\\':
                pos += 2
            else:
                if ch == '"':
                    in_str = not in_str
                else:
                    if line[pos:pos+2] == '//' and not in_str:
                        return line[:pos]
                pos += 1
        return line
    s = re.sub(r'^.*//.*$', rm_cm, s, flags=re.MULTILINE)  # re.MULTILINE for ^$
    s = re.sub(r'{\s*,', r'{', s)
    s = re.sub(r',\s*}', r'}', s)
    s = re.sub(r'\[\s*,', r'[', s)
    s = re.sub(r',\s*\]', r']', s)
    try:
        ans = json.loads(s, *args, **kwargs)
    except Exception:
        print('Error on load json.')
        ans = None
    return ans


class Setting:

    meta_info = [
            {"opt": "task_bullet_open",
             "cmt": ["Character of opened task, one of:",
                    " - | ❍ | ❑ | ■ | □ | ☐ | ▪ | ▫ | – | — | ≡ | → | › | [ ]"],
             "def": "☐",
             "frm": "strs",
             "lst": ["-", "❍", "❑", "■", "□", "☐", "▪", "▫", "–", "—", "≡", "→", "›", "[ ]"]
             },
            {"opt": "task_bullet_done",
             "cmt": ["Character of completed task, one of:",
                    " + | ✓ | ✔ | √ | [x]"],
             "def": "✔",
             "frm": "strs",
             "lst": ["+", "✓", "✔", "√", "[x]"]
             },
            {"opt": "task_bullet_cancel",
             "cmt": ["Character of cancelled task, one of:",
                    " x | ✘ | [-]"],
             "def": "✘",
             "frm": "strs",
             "lst": ["x", "✘", "[-]"]
             },
            {"opt": "date_format",
             "cmt": ["Format of date/time. Possible macro characters are:",
                     "  %a: First three characters of the weekday, e.g. Wed.",
                     "  %A: Full name of the weekday, e.g. Wednesday.",
                     "  %B: Full name of the month, e.g. September.",
                     "  %w: Weekday as a number, from 0 to 6, with Sunday being 0.",
                     "  %m: Month as a number, from 01 to 12.",
                     "  %p: AM/PM for time.",
                     "  %y: Year in two-digit format, that is, without the century. For example, '19' instead of '2019'.",
                     "  %Y: Year in four-digit format. For example '2019'.",
                     "  %f: Microsecond from 000000 to 999999.",
                     "  %Z: Timezone.",
                     "  %z: UTC offset.",
                     "  %j: Number of the day in the year, from 001 to 366.",
                     "  %W: Week number of the year, from 00 to 53, with Monday being counted as the first day of the week.",
                     "  %U: Week number of the year, from 00 to 53, with Sunday counted as the first day of each week.",
                     "  %c: Local date and time version.",
                     "  %x: Local version of date.",
                     "  %X: Local version of time."],
             "def": "(%y-%m-%d %H:%M)",
             "frm": "str",
             },
            {"opt": "archive_name",
             "cmt": ["Caption which is inserted above archived tasks"],
             "def": "Archive:",
             "frm": "str",
             },
            {"opt": "add_created_tag",
             "cmt": ["When creating new task, add tag @created"],
             "def": True,
             "frm": "bool",
             },
            {"opt": "done_tags",
             "cmt": ["When task is changed between Done/Cancelled, add tag @done/@canceled"],
             "def": True,
             "frm": "bool",
             },
            {"opt": "done_date",
             "cmt": ["When task is changed between Done/Cancelled, add timestamp"],
             "def": True,
             "frm": "bool",
             }
            ]

    def __init__(self):
        self.default = {item['opt']: item['def'] for item in self.meta_info}

        if not os.path.exists(config_file):
            with open(config_file, "w") as wf:
                json.dump({}, wf, indent=4)

        self.get_cfg()

    def get_cfg(self):
        with open(config_file, encoding='utf8') as rf:
            # cfg = json.load(rf)
            cfg = _json_load(rf.read())

            def get(key):
                return cfg.get(key, self.default[key])

            self.task_bullet_open = get('task_bullet_open')
            self.task_bullet_done = get('task_bullet_done')
            self.task_bullet_cancel = get('task_bullet_cancel')
            self.space_before_tag = ' '

            self.date_format = get("date_format")
            self.archive_name = get("archive_name")
            self.done_date = get('done_date')
            self.done_tags = get("done_tags")

            self.add_created_tag = get("add_created_tag")
            if self.done_tags:
                self.done_tag = "@done"
                self.cancel_tag = "@cancelled"
            else:
                self.done_tag = ""
                self.cancel_tag = ""

    def config(self):
        subset = ''  # section in user.json, if user.json is used
        title = 'Plain Tasks options'
        how = {'hide_lex_fil': True, 'stor_json': fn_config}
        op_ed.OptEdD(
            path_keys_info=self.meta_info,
            subset=subset,
            how=how
            ).show(title)
        self.get_cfg()  # plugin function to reread options
