# Having Fun with the Play Pattern Timed command
# Mehackit 2016
vbeat = 1
vbpm = 80
vpit = 4
vvar = 2 #dur(2)/moll(1)- Variante
vins = 3 #instrumentation
vvol = 1 #Lautstärke

#set :a, 127
#set :previous_cc_value, get[:a]
variante7= :minor7
variante3= :minor

OSCverbindung = "/osc:172.16.185.26:58132/bilddaten"

besetzung = :piano

live_loop :datenabfragen do
  empfangenedaten = sync OSCverbindung
  name = empfangenedaten[0].split(":")[0]
  wert = empfangenedaten[0].split(":")[1]
  if (name == "dominant_color")
    print "dominante Farbe"
  elsif(name == "brightness")
    print "helligkeit"
  elsif(name == "contrast")
    print "Kontrast"
  elsif(name == "saturation")
    print "Sättigung"
  elsif(name == "sharpness")
    print "Schärfe"
  end
  
end




live_loop :melodia do
  use_bpm vbpm
  with_fx :reverb, mix: 0.4 do
    variante #fragt ab, ob dur oder moll
    instrumentation #fragt Instrument ab
    
    use_synth besetzung
    
    play chord(:C4+vpit, variante3), release: 2, amp: 0.5+vvol
    play_pattern_timed chord(:C3+vpit, variante7), 0.25, release: 0.05, amp: vvol
    play_pattern_timed chord(:C4+vpit, variante7), 0.25, release: 0.1, amp: vvol
    play_pattern_timed chord(:C5+vpit, variante7), 0.25, release: 0.2, amp: vvol
    play_pattern_timed chord(:C6+vpit, variante7), 0.25, release: 0.3, amp: vvol
  end
end

live_loop :hithat do
  use_bpm vbpm
  if(vbeat== 1)
    beat1
  elsif(vbeat== 2)
    beat2
  else(vbeat== 3)
    beat3
  end
end

define :variante do
  if (vvar==1)
    variante7 = :minor7
    variante3 = :minor
  elsif (vvar==2)
    variante7 = :major7
    variante3 = :major
  end
end

define :instrumentation do
  if (vins==1)
    besetzung = :piano
  elsif (vins==2)
    besetzung = :tri
  elsif (vins==3)
    besetzung = :saw
  elsif (vins==4)
    besetzung = :piano
  elsif (vins==5)
    besetzung = :piano
  end
  
end




define :beat1 do
  sample :drum_heavy_kick
  sleep 0.5
  sample :drum_heavy_kick
  sleep 0.5
  sample :drum_snare_hard
  sleep 1
end
define :beat2 do
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


define :beat3 do
  in_thread do
    
    sleep 0.5
    with_fx :reverb, mix: 0.3 do
      3.times do
        sample :drum_cymbal_closed, rate: 1.5, vol: rrand(0.3, 0.7)
        sleep 0.5
      end
      sample :perc_snap , rate: 2, vol: rrand(0.1, 0.3)
    end
  end
  use_bpm vbpm
  sample :bd_haus
  sleep(1)
end
