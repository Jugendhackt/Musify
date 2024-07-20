use_bpm 120
set :beat, 2
set :geschwindigkeit, 3
set :a, 127
set :previous_cc_value, get[:a]


live_loop :midi_piano do
  use_real_time
  note, velocity = sync "/midi:arturia_keystep_32_2:13/note_on"
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

live_loop :lautstärkeregler do
  use_real_time
  cc_value = sync "/midi:arturia_keystep_32_2:13/control_change"
  set :a, cc_value[1]
  set :previous_cc_value, :a
  set :geschwindigkeit, ((get[:a] + 40) / 40.0) - 1
  
end

live_loop :beateinstellen do
  cc, value = sync "/midi:midiin2_(monologue)_2:1/control_change"
  
  
  
  define :play_beat_1 do
    sample :drum_heavy_kick
    sleep 0.5
    sample :drum_heavy_kick
    sleep 0.5
    sample :drum_snare_hard
    sleep 1
  end
  define :play_beat_2 do
    sample :drum_heavy_kick
    sleep 0.25
    sample :drum_heavy_kick
    sleep 0.25
    sample :drum_heavy_kick
    sleep 0.25
    sample :drum_heavy_kick
    sleep 0.25
    sample :drum_snare_hard
    sleep 0.5
    sample :drum_snare_hard
    sleep 0.5
  end
  define :play_beat_3 do
    sample :drum_heavy_kick
    sleep 0.5
    sample :drum_heavy_kick
    sleep 0.5
    sample :drum_snare_hard
    sleep 1
  end
  define :play_beat_4 do
    sample :drum_heavy_kick
    sleep 0.5
    sample :drum_heavy_kick
    sleep 0.5
    sample :drum_snare_hard
    sleep 1
  end