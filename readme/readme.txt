Plain Tasks plugin for CudaText

Installation

    install lexer ToDo (required by plugin, not included in this repo)
    install plugin Plain Tasks

Projects

    Anything with colon at the end of the line is a project title
    Projects can be nested inside each other
    Projects can be folded (a built-in editor feature)

Work with tasks
Create tasks

    command: Plain Tasks/New adds a new task
    Alt+I also adds a new task
    If you’re on a new line, plugin creates a new task on the current line
    If you’re on a line with a task, pressing new task shortcut adds a task after it
    If you’re on a line with some normal text, pressing new task shortcut converts it to a task
    New tasks are nested as much as the task on the previous line
    If option "add_created_tag"=true, also add tag @created with timestamp

Complete tasks

    command: Plain Tasks/Complete marks a task as done @done(19-12-24 01:10)
    Alt+D also marks a task as done @done(19-12-24 01:06)
    Pressing Alt+D again puts it back in pending mode
    If option "done_tags"=true, also add tag @done
    If option "done_date"=true, also add timestamp

Cancel tasks

    command: Plain Tasks/Cancel marks the task as cancelled @cancelled(19-12-24 01:12)
    Alt+C marks the task as cancelled @cancelled(19-12-24 01:12)
    Pressing Alt+C again puts it back in pending mode
    If option "done_tags"=true, also add tag @cancelled
    If option "done_date"=true, also add timestamp

Tagging tasks

    You can add tags using @ sign, like this @tag

Archiving tasks

    command: Plain Tasks/Archive archives tasks in done mode (completed or cancelled tasks).
    Alt+Shift+A archives tasks in done mode (completed or cancelled tasks).
    It does it by removing them from your list and appending them to the bottom of the file under Archive project.
    The archive project is separated from the other list of projects with a line. See bottom of this file.

Priority

    type c, press Tab key — it’ll become @critical
    type h, press Tab key — it’ll become @high
    type l, press Tab key — it’ll become @low
    type t, press Tab key — it’ll become @today

Time tracking

    type s, press Tab key — it’ll become @started(19-12-24 01:22). You’ll get a current date and time; When a task with such tag is completed/cancelled, plugin will calculate the time spent on that task.
    type tg, press Tab key — @toggle(14-10-13 16:14). That way you can pause and resume started task, so result of calculation will be more correct. First, you need start task, then toggle means pause, next toggle — resume, etc.
    type cr, press Tab key — @created(14-12-24 15:57).

File types

Plugin supports these file types out of the box:

    TODO
    *.todo
    *.todolist
    *.taskpaper
    *.tasks

Settings

To configure plugin, call menu item "Options / Settings - plugins / Plain Tasks / Config..."

About

    Author: OlehL, https://github.com/OlehL
    License: MIT
