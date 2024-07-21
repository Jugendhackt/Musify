from pythonosc import udp_client

ip = "172.16.185.26"
#unter I/O lokale ip adresse
port = 4560
#unter I/O osc port, beides in sonic pi
client = udp_client.SimpleUDPClient(ip, port)

channel = 0
pitch = 90
sonic_pi_code = f"control get(:synth), pitch: {pitch}"

client.send_message('/run-code', sonic_pi_code)
print("Nachricht an Sonic Pi gesendet.")

#nachricht lässt sich mit 
#live_loop :osc_debug do
#  use_real_time
#  msg = sync "/osc*/run-code"
#  puts msg
#end
#aufrufen