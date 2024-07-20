use_bpm 120
set :beat, 2
set :geschwindigkeit, 3
set :a, 127
set :lautstärke, 1
set :previous_cc_value, get[:a]

#Geschwindigkeit = DRIVE
#Noten = Tasten
#Lautstärke = VCO2 Shape
#Beats = LFO Rate

live_loop :midi_piano do
  use_real_time
  note, velocity = sync "/midi:midiin2_(monologue)_1:1/note_on"
  synth :piano, note: note, amp: velocity / 127.0  # Normiere den Wert auf den Bereich 0.0 bis 1.0
end

live_loop :hihat do
  use_bpm get[:geschwindigkeit] * 50
  if(get[:beat] == 1)
    play_beat_1
  elsif(get[:beat] == 2)
    play_beat_2
  elsif(get[:beat] == 3)
    play_beat_3
  else
    play_beat_4
  end
end

live_loop :geschwindigkeit do
  use_real_time
  cc_value = sync "/midi:midiin2_(monologue)_1:1/control_change" #DRIVE
  set :a, cc_value[1]
  set :previous_cc_value, :a
  if (get[:a] > 40)
    set :geschwindigkeit, ((get[:a] + 40) / 40.0) - 1
  else
    set :geschwindigkeit, 1
  end
end

live_loop :abfragen do
  cc, value = sync "/midi:midiin2_(monologue)_1:1/control_change"
  if (cc == 24) #Korg Monolog LFO Rate
    b = (value / 43.0).round + 1
    set :beat, b
    if (get[:beat] == 0)
      set :beat, 1
    end
  end
  if (cc == 37) #Korg Monolog VCO2 Shape
    set :lautstärke, value / 127.0
  end
end
live_loop :osc_debug do
  use_real_time
  msg = sync "/osc*/run-code"
  puts msg
end
define :play_beat_1 do
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_snare_hard, amp: get[:lautstärke]
  sleep 1
end
define :play_beat_2 do
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.25
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.25
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.25
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.25
  sample :drum_snare_hard, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_snare_hard, amp: get[:lautstärke]
  sleep 0.5
end
define :play_beat_3 do
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_snare_hard, amp: get[:lautstärke]
  sleep 1
end
define :play_beat_4 do
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_heavy_kick, amp: get[:lautstärke]
  sleep 0.5
  sample :drum_snare_hard, amp: get[:lautstärke]
  sleep 1
end