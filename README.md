# How to Use cuda_plain_tasks:
  * need install lexer ToDo
  * need instsll plugin cuda_plain_tasks

  ## Projects:
    ☐ Anything with colon at the end of the line is a project title
    ☐ Projects can be nested inside each other
    ☐ Projects can be folded (a built-in editor feature)

  ## Tasks:
    New:
      ☐ command: PlainTasks/New  add a new task
      ☐ Alt+i also adds a new task
      ☐ If you’re on a new line cuda_plain_tasks creates a new task on the current line
      ☐ If you’re on a line with a task pressing new task shortcut adds a task after it
      ☐ If you’re on a line with some normal text pressing new task shortcut converts it to a task
      ☐ New tasks are nested as much as the task on the previous line
      ☐ If option "add_created_tag"=true also add tag @created with timestamp
    Complete:
      ✔ command: PlainTasks/Complete  marks a task as done @done(19-12-24 01:10)
      ✔ Alt+d also marks a task as done @done(19-12-24 01:06)
      ☐ Pressing Alt+d again puts it back in pending mode
      ☐ If option "done_tags"=true also add tag @done
      ☐ If option "done_date"=true also add timestamp
    Cancel:
      ✘ command: PlainTasks/Cancel marks the task as cancelled @cancelled(19-12-24 01:12)
      ✘ Alt+c marks the task as cancelled @cancelled(19-12-24 01:12)
      ☐ Pressing Alt+c again puts it back in pending mode
      ☐ If option "done_tags"=true also add tag @cancelled
      ☐ If option "done_date"=true also add timestamp
    Tagging:
      ☐ You can add tags using @ sign, like this @tag
    Archiving:
      ✘ command: PlainTasks/Archive archives tasks in done mode (completed or cancelled tasks).
      ☐ Alt+shift+A archives tasks in done mode (completed or cancelled tasks).
        It does it by removing them from your list and appending them to the bottom
        of the file under Archive project.
        The archive project is separated from the other list of projects with a line.
        See bottom of this file.
  ![](https://media.giphy.com/media/RN9Aqa8Aat4MRGW7d3/giphy.gif)

  ## Priority:
    ☐ type c, press tab key — it’ll become @critical
    ☐ type h, press tab key — it’ll become @high
    ☐ type l, press tab key — it’ll become @low
    ☐ type t, press tab key — it’ll become @today
   ![](https://i.imgur.com/ITJ2Ql8.png)

  ## Time Tracking:
    ☐ type s, press tab key — it’ll become @started(19-12-24 01:22)
      You’ll get a current date and time; When a task with such tag is completed/cancelled,
      cuda_plain_tasks will calculate the time spent on that task.
    ☐ type tg, press tab key — @toggle(14-10-13 16:14)
      That way you can pause and resume started task, so result of calculation will be more correct.
      First, you need start task, then toggle means pause, next toggle — resume, etc.
    ☐ type cr, press tab key — @created(14-12-24 15:57)
  ![](https://media.giphy.com/media/kIF5xIqz8dmdnW4cTF/giphy.gif)

  ## FileType Support:
    cuda_plain_tasks support these file types out of the box
    ✔ TODO
    ✔ *.todo
    ✔ *.todolist
    ✔ *.taskpaper
    ✔ *.tasks

  # Settings:
    ☐ goto: Options / Settings - plugins / PlainTasks / Config...
