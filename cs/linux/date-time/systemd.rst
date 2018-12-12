timedatectl
===========
overview
--------
- timedatectl is a systemd CLI, to control system time, timezone, ntp
  synchronization, etc.

subcommands
-----------
status
^^^^^^
- show various time status:

  * local time

  * UTC time

  * RTC time

  * timezone

  * whether system clock is in sync with NTP (例如正在同步, 但尚未完成同步).

  * NTP service status

  * RTC timezone

show
^^^^
ditto in machine-readable format.

set-time
^^^^^^^^
::

  set-time "YYYY-MM-DD HH:mm:SS"

- set system time, also update RTC.

set-local-rtc
^^^^^^^^^^^^^
::

  set-local-rtc {0|1}

- If "0", the system is configured to maintain the RTC in universal time. If
  "1", it will maintain the RTC in local time instead.

  UTC is recommended.

- This command will change the 3rd line of /etc/adjtime.

options
"""""""
- ``--adjust-system-clock`` By default, RTC is also synced from system clock.
  When this option is passed, the system clock is synchronized from the RTC.

set-ntp
^^^^^^^
::

  set-ntp {0|1}

- enable/disable NTP.

- If 1, this enables and starts the first existed service listed in the
  environment variable SYSTEMD_TIMEDATED_NTP_SERVICES of
  systemd-timedated.service. If 0, disable and stop the aforementioned
  service.

set-timezone
^^^^^^^^^^^^
::

  set-timezone TZ

- If the RTC is configured to be in the local time, this will also update the
  RTC time.

- This changes ``/etc/localtime`` symlink.

list-timezones
^^^^^^^^^^^^^^
show available timezones. can be used in set-timezone.

timesync-status
^^^^^^^^^^^^^^^
Show systemd-timesyncd.service's status.

including:

- NTP server in use.

options
"""""""
- ``--monitor``. continuously monitor status output.

show-timesync
^^^^^^^^^^^^^
ditto in machine-readable format.

- ``--all``. By default, empty properties are suppressed. Use --all to show
  those too.

- ``--property=NAME``. only show the specified property. can be specified
  multiple times.

- ``--value``. only print the value, and skip the property name.

systemd-timesyncd
=================

overview
--------
- systemd-timesyncd is a daemon for synchronizing the system clock across the
  network.

mechanism
---------
- It implements an SNTP client. This only implements a client side, and does
  not bother with the full NTP complexity, focusing only on querying time from
  one remote server and synchronizing the local clock to it.

- The daemon runs with minimal privileges, and has been hooked up with
  systemd-networkd to only operate when network connectivity is available.

- The daemon saves the current clock to disk every time a new NTP sync has been
  acquired, and uses this to possibly correct the system clock early at bootup,
  in order to accommodate for systems that lack an RTC such as the Raspberry Pi
  and embedded devices, and make sure that time monotonically progresses on
  these systems

configuration
-------------
- /etc/systemd/timesyncd.conf

- how is NTP server determined:

  * Any per-interface NTP servers obtained from systemd-networkd.service(8)
    configuration or via DHCP take precedence.
  
  * The NTP servers defined in /etc/systemd/timesyncd.conf will be appended to
    the per-interface list at runtime and the daemon will contact the servers
    in turn until one is found that responds.
  
  * If no NTP server information is acquired after completing those steps, the
    NTP server host names or IP addresses defined in FallbackNTP= will be used.

References
==========
- timedatectl(1)

- systemd-timesyncd
  https://wiki.archlinux.org/index.php/systemd-timesyncd
