# Clip-Master
Python based program with a GUI interface to expedite extracting video clips from multiple video files.
The program was designed to extract game play clips from multiple saved game play recordings and automatically store them
for later use in montages, etc to be uploaded to YouTube.

### Project Current State

This is my first project that I am doing through GitHub. Happy for any help/guidance in general Github setup and in the
coding of the program itself. The program is functional at a base level with known flaws which I will work through over the
next few days/weeks.

The completed project will allow the user to do the following:
- Open videos in a VLC player in succession and mark in and out positions for clips they want extracted.
- Input a title for each particular clip as they are marked.
- Use ffmpeg to extract each clip in a batch process.
- Save extracted clips to a particular directory.
- Move videos that have been processed into a different directory.
- Recode to different supported file formats.

### Usage

- Add a web interface to your VLC player (I'll add detailed description when I have time).
- Open the ClipMaster.py file in a text editor and set the user parameters at the top of the file. If these
parameters are not set, it is unlikely the program will work.
- Run the program by executing 'python ClipMaster.py'. you should see the Clip Master window appear.
- Open your video (needs to be .mp4 at this stage. other file formats to follow).
- Mark the start position for the clip you wish to extract by clicking the 'Mark clip' button.
- Mark the end position for the clip with the 'Mark Clip' button.
- Enter a clip title in the box provided and click 'Save clip for processing'
- Mark as many clips as you like in as many files as you like (need to be in the same directory).
- Once all clips are marked, click the 'Finish and process marked clips' button.
- Sit back and chill while all your clips are extracted.

### Things to do...

This project is in early development and has known flaws. Items to be worked on in the near future include:
- File name checking prior to invoking ffmpeg. Some characters cause crashes.
- Multi file type (relatively easy) and potentially recoding to different file types.
- Better error/exception catching and management.




