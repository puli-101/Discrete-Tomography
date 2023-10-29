clean:
	rm -rf output/*

clean-vid:
	rm -rf videos/*

clean-all:
	rm -rf output/* videos/*

video:
	mkdir -p videos
	ffmpeg -framerate 5 -pattern_type glob -i 'output/*.bmp' -c:v libx264 -pix_fmt yuv420p out.mp4
