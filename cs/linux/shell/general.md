# shell

-   a shell is simply a macro processor *program* that executes commands.

    In essence, a shell program is no different than any other program. You
    can achieve everything a shell does by writing a program manually that
    utilizes Linux rules and APIs.

-   Files containing commands can be created, and become commands themselves.

-   shells may be used interactively or non-interactively.

-   command execution can be synchronous and asynchronous.

    *   synchronous: blocking operation, waiting for subprocess to exit.

    *   asynchronous: event driven, spawn subprocess then return, continue
        on other matters, notified when SIGCHLD signal is sent back.
