PYTHON SLIDE SHOW

This script provides a way to view in full screen mode all the images in a directory
as a slide show.

The script will cycle through the images indefinitely unless you either
press escape or the "q" key.

To pause the slide show, press the space bar.

To move forward or backward one image, use the left or right arrow.

Each image is resized such that it fills the screen either vertically or
hozizontally, depending on the aspect ratio of the image.

Features:
1. Specify a directory
2. Specify a duration each image will be on screen
3. Specify a duration for the dissolve between images.

The default duration to show each image is five seconds.
The default dissolve duration is one second.

Usage:
python3 slide_show.py sample_images

By adding arguments, you can change the duration each image is displayed,
and change the duration of the dissolve between images:

python3 slide_show.py sample_images 10 2

In the command above, each image is displayed for 10 seconds, and each dissolve
has a duration of 2 seconds.
