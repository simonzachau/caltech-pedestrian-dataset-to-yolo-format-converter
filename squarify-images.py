import glob
import Image

frame_size = (640, 640)
directory = 'images'

for frame in sorted(glob.glob(directory + '/*.png')):
	# enlarge 640 x 480 frames up to frame_size 
	# by filling the bottom area with whitespace
	new_frame = Image.new('RGB', frame_size, 'white')
	new_frame.paste(Image.open(frame), (0, 0))

	new_frame_path = frame.replace('.png', '_squared.png')
	new_frame.save(new_frame_path, 'png')

	print('saved ' + new_frame_path)