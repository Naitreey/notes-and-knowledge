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
