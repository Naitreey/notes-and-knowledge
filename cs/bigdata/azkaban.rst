overview
========
- Azkaban is a distributed workflow manager to run Hadoop jobs (and maybe any
  job).

- Azkaban resolves the ordering through job dependencies and provides an easy
  to use web user interface to maintain and track your workflows.

installation
============
two modes
---------
* solo-server mode.
  
  - the DB is embedded H2 and both web server and executor server run in the
    same process.

* distributed multiple-executor mode.
  
  - for most serious production environment.
    
  - Its DB should be backed by MySQL instances with master-slave set up.

  - The web server and executor servers should ideally run in different hosts
    so that upgrading and maintenance shouldn’t affect users.

multiple-executor mode
----------------------
- 下载源代码, 编译::

    git clone https://github.com/azkaban/azkaban.git
    git checkout <tag>
    ./gradlew build -x test

- create azkaban database and user::

    CREATE DATABASE azkaban;
    CREATE USER '<username>'@'%' IDENTIFIED BY 'password';
    GRANT SELECT,INSERT,UPDATE,DELETE ON azkaban.* to '<username>'@'%' WITH GRANT OPTION;

- increase mysql max packet size::

    [mysqld]
    max_allowed_packet=1024M

- create azkaban tables. 解压 ``azkaban-db/build/distributions/azkaban-db-*.tar.gz``,
  执行 ``create-all-sql-*.sql``::

    mysql -u root azkaban <create-all-sql-*.sql

- 指定一个将要安装 azkaban executor 的目录. 将 ``azkaban-exec-server-*.tar.gz``
  解压进去.::

    tar -x -f azkaban-exec-server-*.tar.gz --strip-components=1

- 修改配置 ``conf/azkaban.properties`` 里面::

    mysql.user=<username>
    mysql.password=<password>

- 启动 executor server::

    ./bin/start-exec.sh

- activate the executor by calling::

    curl -G "localhost:$(<executor.port)/executor?action=activate"

- 指定一个将要安装 azkaban web server 的目录 (与 executor server 不能相同). 将
  ``azkaban-web-server-*.tar.gz`` 解压进去.::

    tar -x -f azkaban-web-server-*.tar.gz --strip-components=1

- 修改配置.

- 启动 web server::

    bin/start-web.sh

plugins
=======
Azkaban is designed to make non-core functionalities plugin-based, so that

- they can be selectively installed/upgraded in different environments without
  changing the core Azkaban,
  
- it makes Azkaban very easy to be extended for different systems.

user manager plugins
--------------------
- specify ``user.manager.class`` property in
  ``web-server-dir/conf/azkaban.properties``.

- put the containing jar in ``plugins`` directory.

viewer plugins
--------------
- specify ``viewer.plugins`` property in ``web-server-dir/conf/azkaban.properties``.
  its value is a directory name under ``plugins/viewer/`` directory.

hdfs viewer
^^^^^^^^^^^
parameters
""""""""""
- azkaban.should.proxy

- hadoop.security.manager.class

- proxy.user

- proxy.keytab.location

job type plugins
----------------
- built-in job types to run local unix commands and simple java programs

- specify ``azkaban.jobtype.plugin.dir`` in
  ``exec-server-dir/conf/azkaban.properties``.

configuration
=============
web server configurations
-------------------------
general
^^^^^^^
- azkaban.name. The name of the azkaban instance that will show up in the UI.
  default "Local".

- azkaban.label. A label to describe the Azkaban instance. default "My Local
  Azkaban".

- azkaban.color. Hex value that allows you to set a style color for the Azkaban
  UI. #FF3601.

- web.resource.dir. Sets the directory for the ui’s css and javascript files.
  default "web".

- default.timezone. The timezone that will be displayed by Azkaban.  default
  America/Los_Angeles

- viewer.plugin.dir. Directory where viewer plugins are installed. default
  "plugins/viewer".

- job.max.Xms. The maximum initial amount of memory each job can request. This
  validation is performed at project upload time. default 1GB

- job.max.Xmx. The maximum amount of memory each job can request. This
  validation is performed at project upload time. default 2GB

multiple executor mode parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

jetty parameters
^^^^^^^^^^^^^^^^

project manager settings
^^^^^^^^^^^^^^^^^^^^^^^^

database connection parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- database.type. The database type. Currently, the only database supported is
  mysql. default mysql.

- mysql.port. The port to the mysql db. default 3306

- mysql.host. The mysql host. default localhost

- mysql.database. The mysql database.

- mysql.user. The mysql user.

- mysql.password. The mysql password.

- mysql.numconnections. The number of connections that Azkaban web client can
  open to the database, default 100

executor manager properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^

notification email properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- mail.sender. sender address.

- mail.host.

- mail.user.

- mail.password.

user manager properties
^^^^^^^^^^^^^^^^^^^^^^^
- user.manager.class. The user manager that is used to authenticate a user.
  default azkaban.user.XmlUserManager

- user.manager.xml.file. xml file for XmlUserManager. default
  "conf/azkaban-users.xml".

- Any additional parameters required by your custom user manager.

user session properties
^^^^^^^^^^^^^^^^^^^^^^^

executor server configurations
------------------------------
database connection parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See above.


user manager
============

XmlUserManager
--------------
- By default, Azkaban ships with the XMLUserManager class which authenticates
  users based on ``web-server-dir/conf/azkaban-users.xml``.

plugins
-------
See `user manager plugins`_.

configuration
-------------
See `user manager properties`_.

using Azkaban
=============
creating flows
--------------
steps
^^^^^
1. Create a file called ``flow20.project``. Add ``azkaban-flow-version`` to
   indicate this is a Flow 2.0 Azkaban project::

     azkaban-flow-version: 2.0

2. Create a ``basic.flow`` file, with a section called ``nodes``, containing
   all jobs to run.

3. zip the archive. Do not zip the directory containing the created files.

4. Upload archive to created project.

job node configuration
^^^^^^^^^^^^^^^^^^^^^^
Job node configurations is located under ``nodes`` top-level key.

- ``name``. job's name.

- ``type``. job's type.

- ``dependesOn``. a list of all parent jobs of this job.

- ``config``. a dict of configurations required by a specific job type.

common configuration paramters under config key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``retries``. The number of retries that will be automatically attempted for
  failed jobs.

- ``retry.backoff``. The millisec time between each retry attempt

- ``working.dir``. Override the working directory for the execution. This is by
  default the directory that contains the job file that is being run.

- ``env.<name>``. Set the named environment variable

- ``failure.emails``. Comma delimited list of emails to notify during a
  failure.

- ``success.emails``. Comma delimited list of emails to notify during a
  success.

- ``notify.emails``. Comma delimited list of emails to notify during either a
  success or failure.

flow configuration
^^^^^^^^^^^^^^^^^^
Global flow configurations is located under ``config`` top-level key. 这里的每
个配置项相当于是 job node configuration 的全局 fallback value.

embedded flows
^^^^^^^^^^^^^^
A job node can embed an entire subflow, by specifying ``nodes`` key under a job
node's specification.

conditional workflow
^^^^^^^^^^^^^^^^^^^^
- Conditional workflow feature allows users to specify whether to run certain
  jobs based on conditions.

- Condition is specified after ``condition`` key. A valid condition is a
  combination of multiple conditions on job runtime parameters and one
  condition on job status macro.

  * condition on job runtime paramters. Jobs need to write runtime parameters
    into ``$JOB_OUTPUT_PROP_FILE``. Parameters are accessed via
    ``${jobName:param}`` syntax.

  * condition on job status macro. supported:
    ``all_success, all_done, all_failed, one_success, one_failed``.

  * Comparison and logical operators can be used to connect individual condition
    components. Supported operators: ``==, !=,  >, >=, <, <=, &&, ||, !``.

runtime parameters
^^^^^^^^^^^^^^^^^^
- Use ``${parameter}`` in ``basic.flow`` definition file to access value of any
  parameters available at runtime.

- 对于一个 job, 它可用的 parameters 包含:

  * metadata parameters made available by azkaban (see below).

  * 这个 job 本身的 ``config`` key 和从全局 ``config`` 继承的所有参数.

  * parent jobs' output parameters written to their ``$JOB_OUTPUT_PROP_FILE``.

  这些参数全部通过 ``$JOB_PROP_FILE`` 文件提供给 job. 并且可通过
  ``${parameter}`` 语法来获取和使用.

- The following parameters are made available to job automatically at runtime.

  * azkaban.job.attempt. The attempt number for the job. Starts with attempt 0
    and increments with every retry.

  * azkaban.job.id. The job name.

  * azkaban.flow.flowid. The flow name that the job is running in.

  * azkaban.flow.execid. The execution id that is assigned to the running flow.

  * azkaban.flow.projectid. The numerical project id.

  * azkaban.flow.projectversion. The project upload version.

  * azkaban.flow.uuid. A unique identifier assigned to a flow’s execution.

  * azkaban.flow.start.timestamp. The millisecs since epoch start time.

  * azkaban.flow.start.year. The start year.

  * azkaban.flow.start.month. The start month of the year (1-12)

  * azkaban.flow.start.day. The start day of the month.

  * azkaban.flow.start.hour. The start hour in the day.

  * azkaban.flow.start.minute. The start minute.

  * azkaban.flow.start.second. The start second in the minute.

  * azkaban.flow.start.milliseconds. The start millisec in the sec

  * azkaban.flow.start.timezone. The start timezone that is set.

uploading project files
-----------------------
- The project files are packaged into an archive file, then uploaded to
  Azkaban.

- Supported archive formats: zip.

- The zip should contain the ``*.job`` files and any files needed to run your
  jobs. Job names must be unique in a project.

- Azkaban will validate the contents of the zip to make sure that dependencies
  are met and that there’s no cyclical dependencies detected. If it finds any
  invalid flows, the upload will fail.

- Uploads overwrite all files in the project. Any changes made to jobs will be
  wiped out after a new zip file is uploaded.

executing flow
--------------
- disable/enable jobs. From the Flow View panel, you can right click on the
  graph and disable or enable jobs. Disabled jobs will be skipped during
  execution as if their dependencies have been met. Disabled jobs will appear
  translucent.

- email override. Azkaban will use the default notification emails set in the
  final job in the flow. If overridden, a user can change the email addresses
  where failure or success emails are sent. The list can be delimited by
  commas, whitespace or a semi-colon.

- failure options.
  
  * Finish Current Running: will finish the jobs that are currently running,
    but it will not start new jobs. The flow will be put in the FAILED
    FINISHING state and be set to FAILED once everything completes.

  * Cancel All: will immediately kill all running jobs and set the state of the
    executing flow to FAILED.

  * Finish All Possible: will keep executing jobs in the flow as long as its
    dependencies are met. The flow will be put in the FAILED FINISHING state
    and be set to FAILED once everything completes.

- concurrent options.

  * Skip Execution option will not run the flow if its already running.

  * Run Concurrently option will run the flow regardless of if its running.
    Executions are given different working directories.

  * Pipeline runs the the flow in a manner that the new execution will not
    overrun the concurrent execution.

    - Level 1: blocks executing job A until the the previous flow’s job A has
      completed.

    - Level 2: blocks executing job A until the the children of the previous
      flow’s job A has completed. This is useful if you need to run your flows
      a few steps behind an already executing flow.

- flow parameters. Allows users to override flow parameters. The flow
  parameters override the global properties for a job, but not the properties
  of the job itself.

flow execution page
-------------------
- Cancel - kills all running jobs and fails the flow immediately. The flow
  state will be KILLED.

- Pause - prevents new jobs from running. Currently running jobs proceed as
  usual.

- Resume - resume a paused execution.

- Retry Failed - only available when the flow is in a FAILED FINISHING state.
  Retry will restart all FAILED jobs while the flow is still active. Attempts
  will appear in the Jobs List page.

- Prepare Execution - only available on a finished flow, regardless of success
  or failures. This will auto disable successfully completed jobs.

schedule flow
-------------
- Any flow options set will be preserved for the scheduled flow.

- scheduling syntax: Quartz syntax.

SLA
---
- SLA -- Service Level Agreement.

- Set SLA notification email or preemption actions.

- Rules can be added and applied to individual jobs or the flow itself.

- If duration threshold is exceeded, then an alert email can be set and/or the
  flow or job can be auto killed. If a job is killed due to missing the SLA, it
  will be retried based on the retry configuration of that job.

job edit
--------
- The changes to the job property parameters will affect an executing flow only
  if the job hasn’t started to run yet. These overwrites of job properties will
  be overwritten by the next project upload.

job logs
--------
- The job logs are stored in the database. They contain all the stdout and
  stderr output of the job.

job types
=========
command
-------
- It runs multiple UNIX commands using java processbuilder. Upon execution,
  Azkaban spawns off a process to run the command.

- configuration:

  * ``command``. The command to run.

  * 若要指定多个命令, specify ``command.1``, ``command.2``, etc., in addition
    to ``command``.

job property precedence
=======================
from lowest to highest.

- ``global.properties`` in ``conf`` directory. global to all jobtypes.

- ``common.properties`` in ``jobtype`` directory. global to all jobtypes.

- ``plugin.properties`` in ``jobtype/<jobtype-name>`` directory. specific to
  a one jobtype.

- global ``config`` in ``basic.flow`` file of a project's zip archive. apply to
  all jobs in the flow.

- flow properties specified at GUI while triggering flow execution. apply to all
  jobs in the flow.

- node-specific ``config`` in ``basic.flow`` file of a project's zip archive.
  apply to a specific job node in the flow.

project permissions
===================
- The user who created a project will be given ADMIN status for the project.

- Adding user permissions gives those users those specified permissions on the
  project. Remove user permissions by unchecking all of the permissions.

- Group permissions allow everyone in a particular group the specified
  permissions. Remove group permissions by unchecking all the group
  permissions.

- If proxy users are turned on, proxy users allows the project workflows to run
  as those users. This is useful for locking down which headless accounts jobs
  can proxy to. They are removed by clicking on the ‘Remove’ button once added.

- supported permissions:

  * ADMIN. Allows the user to do anything with this project, as well as add
    permissions and delete the project.

  * READ. The user can view the job, the flows, the execution logs.

  * WRITE. Project files can be uploaded, and the job files can be modified.

  * EXECUTE. The user is allowed to execute, pause, cancel jobs.

  * SCHEDULE. The user is allowed to add, modify and remove a flow from the
    schedule.
