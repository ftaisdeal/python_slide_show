PYTHON SLIDE SHOW

This script provides a way to view in full screen mode all the images in a directory
as a slide show.

The script will cycle through the images indefinitely unless you either
press escape or the "q" key, both of which quit the program.

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

NOTES

1. The script searches for JPEG, PNG, WEBP, BMP and TIFF files without regard to case or optional spelling, such as JPG or JPEG.
2. The order of the images in the slide show will correspond to the order displayed in the directory on your operating system.
3. When you pause a slide with the space bar, if you then resume the slide show the slide will be displayed for the full duration, as though you had started that slide from the beginning of its full duration again.