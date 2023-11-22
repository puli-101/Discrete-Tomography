INPUT?=videos/video0.avi

OUTPUT?=video

all: bin/convert_pgm

bin/convert_pgm: src/img_handler/convert_pgm.c
	mkdir -p bin
	gcc -o $@ $<

clean:
	rm -rf bin/* compte_rendu.zip

clean-img:
	rm -rf output/*

clean-vid:
	rm -rf videos/*

clean-all:
	rm -rf output/* videos/* sample_results/latest_result.*

mp4:
	ffmpeg -y -i $(INPUT) -c:v mpeg4 videos/$(OUTPUT).mp4 

gif:
	ffmpeg -y -i $(INPUT) -r 15 \
	-vf scale=512:-1 \
	videos/$(OUTPUT).gif

convert:
	convert $(INPUT) sample_results/conversion.png 

zip:
	zip compte_rendu.zip src/misc/* src/img_handler/* src/algorithms.py src/debugging.py src/grid.py src/image.py custom_input/* instances/* main.py makefile README.md

tar:
	tar cvzf compte_rendu.tgz src/misc/* src/img_handler/* src/algorithms.py src/debugging.py src/grid.py src/image.py custom_input/* instances/* main.py makefile README.md

