- OpenSSH is the most used SSH protocol implementation.

- support sshv2, sshv1 support has been removed.

privilege separation
====================
see: https://upload.wikimedia.org/wikipedia/commons/b/be/OpenSSH-Privilege-Separation.svg

Privilege separation is applied in OpenSSH by using several levels of access,
some higher some lower, to run sshd(8) and its subsystems and components.

- a privileged process (root) that listens new connections.
  
- Unpon client connection, a privileged monitor process (root) forked to
  monitor the overall activity with the individual client.

- During initial authentication and network processing stages with the client,
  an unprivileged process (sshd) is forked to handle the contact with the
  remote client.

- After authentication is completed and a session established for user,
  unprivileged sshd process exits. a new user-privileged sshd process (username)
  is forked to handle user traffic, which then forks user's default shell, etc.
