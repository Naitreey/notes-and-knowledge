- wireless driver & firmware. 一些无线网卡不仅需要驱动, 还需要固件.

CLI
===

tools
-----

iw
~~
 
wpa supplicant
~~~~~~~~~~~~~~

.. _wpa_config:

- configuration.

  * For WPA2-enterprise, something at least::
      network={
          ssid="..."
          key_mgmt=WPA-EAP
          identity="<username>"
          password="<password>"
      }
    examples see ``/usr/share/doc/wpa_supplicant``.

netctl
~~~~~~

common operations
-----------------
- status about current link::
    iw dev <dev> link

- statistic information about link::
    iw dev <dev> station dump

- scan network::
    iw dev <dev> scan
  确认加密方式: RSN (WPA2) or WPA, or WEP (如果有 Privacy 字样), or none.
  认证方式: PSK (Personal, 密码) or 802.1x (Enterprise, 用户名密码等).

- connect to network.

  * 无加密或 WEP::
      iw dev <dev> connect <ssid> key 0:<password>

  * WPA, RSN (WPA2)::
      wpa_supplicant [-B] -i <dev> -c <config>
    -B daemon mode. config 为 wpa_config_ 部分的配置.

- IP 地址. 静态或 DHCP. 对于 DHCP::
    dhcpcd <dev>

- Find out which 802.11 protocol the wifi connection is using [UnixSE80211]_::

    iw dev <dev> scan

  * 802.11b AP: there are ``Supported rates`` below 11Mbps.

  * 802.11g AP: there are ``Supported rates`` or ``Extended supported rates``
    above 11Mbps or 6Mbps.

  * 802.11n AP: there is ``HT capabilities`` IE.

  * 802.11ac AP: there is ``VHT`` IE (Very High Throughput).

references
==========

.. [UnixSE80211] `Linux find WiFi Networks protocol(a/b/g/n) version of all available access points <https://unix.stackexchange.com/questions/62265/linux-find-wifi-networks-protocola-b-g-n-version-of-all-available-access-point>`_
