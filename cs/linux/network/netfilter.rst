iptables
========

Saving IPTables Rules
---------------------

Rules created with the iptables command are stored in memory. If the system is
restarted before saving the iptables rule set, all rules are lost. For
netfilter rules to persist through a system reboot, they need to be saved. To
save netfilter rules, type the following command as root:

service iptables save

This executes the iptables init script, which runs the /sbin/iptables-save
program and writes the current iptables configuration to
/etc/sysconfig/iptables. The existing /etc/sysconfig/iptables file is saved as
/etc/sysconfig/iptables.save.

The next time the system boots, the iptables init script reapplies the rules
saved in /etc/sysconfig/iptables by using the /sbin/iptables-restore command.

While it is always a good idea to test a new iptables rule before committing it
to the /etc/sysconfig/iptables file, it is possible to copy iptables rules into
this file from another system's version of this file. This provides a quick way
to distribute sets of iptables rules to multiple machines.

You can also save the iptables rules to a separate file for distribution,
backup or other purposes. To save your iptables rules, type the following
command as root:

iptables-save > <filename>

where <filename> is a user-defined name for your ruleset.

If distributing the /etc/sysconfig/iptables file to other machines, type
/sbin/service iptables restart for the new rules to take effect.

Note the difference between the iptables command (/sbin/iptables), which is
used to manipulate the tables and chains that constitute the iptables
functionality, and the iptables service (/sbin/iptables service), which is used
to enable and disable the iptables service itself.

ipset
=====
- ipset 是唯一能够用一条 iptables 规则表达复杂匹配逻辑、并进行高效匹配的
  iptables extension.

- In order to drop traffic to-from banned networks or IP addresses, use IP sets
  in the raw table of netfilter.

- If you want to change a set without disturbing your existing iptables rules,
  simply swap it with the new set:

  .. code:: sh
    # Create the new set and add the entries to it
    ipset -N new-set ....
    ipset -A new-set ....
    ...
    # Swap the old and new sets
    ipset -W old-set new-set
    # Get rid of the old set, which is now under new-set
    ipset -X new-set

- Iptables matches and targets referring to sets create references, which
  protect the given sets in the kernel. A set cannot be destroyed while there
  is a single reference pointing to it.
