import espeak
es=espeak.ESpeak()
es.say("Jeremy")
es.save("Jeremy and Thomas", "test.wav")
sleep(2)
print("done")
