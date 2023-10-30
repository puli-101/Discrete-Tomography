INPUT?=videos/video0.avi

OUTPUT?=video

clean-img:
	rm -rf output/*

clean-vid:
	rm -rf videos/*

clean-all:
	rm -rf output/* videos/*

mp4:
	ffmpeg -y -i $(INPUT) -c:v mpeg4 videos/$(OUTPUT).mp4 

gif:
	ffmpeg -y -i $(INPUT) -r 15 \
	-vf scale=512:-1 \
	videos/$(OUTPUT).gif
