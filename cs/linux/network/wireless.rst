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
