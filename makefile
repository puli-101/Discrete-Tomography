INPUT?=video0.avi
OUTPUT?=video

clean-img:
	rm -rf output/*

clean-vid:
	rm -rf videos/*

clean-all:
	rm -rf output/* videos/*

mp4:
	ffmpeg -i videos/$(INPUT) -c:v mpeg4 videos/$(OUPUT).mp4

gif:
	ffmpeg -i videos/$(INPUT) -r 15 \
	-vf scale=512:-1 \
	videos/$(OUTPUT).gif
