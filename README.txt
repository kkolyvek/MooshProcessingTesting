* IMPORTANT INSTALLATION INFO FOR MOOSH TRACKER *

===
nginx:
The MooshTracker software uses a custom nginx RTMP server to recieve drone
footage before processing. Downloads are here:

http://nginx-win.ecsds.eu/download/
nginx 1.7.11.3 Gryphon - nginx version that supports our endeavors
vcredist_x86 - supporting file that we also need

https://djp.li/rtmpserver
nginx config file - batch files created by Doug Johnson Productions to make
                    our lives easier
===
ffmpeg:
MooshTracker uses ffmpeg to encode video once processing is done and send it
to an RTMP stream of choice (YouTube or Twitch in this case). Downloads are
here:

https://www.gyan.dev/ffmpeg/builds/
ffmpeg-git-full from the git section - the ffmpeg files we need. You then
need to extract file, and set an allowable path in computer settings. Use
https://windowsloop.com/install-ffmpeg-windows-10/ to help with installation.
===