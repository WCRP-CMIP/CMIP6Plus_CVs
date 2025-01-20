


sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt autoremove -y



sudo apt-get install lighttpd git hostapd dnsmasq iptables-persistent vnstat qrencode php8.2-cgi jq isoquery


sudo apt install python3-pip
sudo apt install python3-psutil
sudo apt install python3-pip


sudo apt-get install dhcpcd5


sudo lighttpd-enable-mod fastcgi-php    
sudo service lighttpd force-reload
sudo systemctl restart lighttpd.service



sudo rm -rf /var/www/html
sudo git clone https://github.com/RaspAP/raspap-webgui/ /var/www/html


sudo nano /etc/resolv.conf

nameserver 8.8.8.8

sudo systemctl restart dnsmasq.service


sudo nano /etc/hostapd/hostapd.conf
country_code = GB

# failed
# psutil 

sudo curl -sL https://install.raspap.com | sudo bash


sudo apt install net-tools
sudo add-apt-repository ppa:kelebek333/kablosu
sudo apt-get update
sudo apt-get install rtl8188fu-dkms



# (Optional) To remove the driver, enter sudo apt purge rtl8188fu-dkms in Terminal and press Enter.


nordvpn login

sudo systemctl status NetworkManager-wait-online.service

sudo apt-get install network-manager
try this in terminal

nmcli device wifi list 
nmcli device wifi connect "$SSID" password "$PASSWORD"




I just wanted to drop this in here in case anyone else had this problem. (I’m using the default rpi wifi card and Ethernet) one day I noticed my speeds had gotten extremely slow (like 0.5 Mbps) and so I checked out the Wireless mode in the hotspot section. The wireless mode was set to 802.11g or something along those lines. I decided to try changing it to 802.11n and boom I was getting 20 Mbps again

You can get even faster throughput with 802.11ac 5GHz wireless. Speeds in the range of 100 Mbps are possible with the RPi's 3b+/4's onboard chipset. Check out this FAQ for more info.
