- cron 和 anacron 的关系.

  cron 负责 ``crontab``, ``cron.d`` 里的项, ``cron.d`` 里一般会有 ``0hourly``,
  用于执行 ``cron.hourly`` 里的项. 由于使用了 ``run-parts``, ``cron.hourly``
  允许使用 ``jobs.allow``, ``jobs.deny`` 来执行或不执行任务.

  anacron 负责 ``anacrontab``, 后者会指定去执行 ``cron.daily``, ``cron.weekly``,
  ``cron.monthly`` 三个目录. 这样是把所有需要 daily/weekly/monthly 执行的任务
  各自合成一个大任务来执行的. 如需细粒度的方式, 则需在 anacrontab 中对每个任务
  注册.

  anacron 不是 daemon, 它要靠在 crontab 中注册, 每小时运行一次, 来检查和执行
  需要的任务. anacron 的注册方式是 ``cron.hourly/0anacron``.
