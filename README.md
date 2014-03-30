ngccat
======

Command line tool to concatenate linuxcnc gcode files.

I've used Blender Cam (blendercam.blogspot.com) for some time now and built this simple tool to concatenate the gcode it generates.  The script concatenates the files by filter out toolchange commands (beware) and line numbering. 
There are also options to add custom commands inbetween the concatenated files (pre&post)


Note that the script is only tested on linuxcnc (emc) gcode and that it is only intended to be used on files that share the same tool.
