import cv2
import math
import random

WINDOW_POSITION = (1050, -33)
WINDOW_SIZE = (500, 295)
BASE_FPS = 33 # FPS to play video at
EARLY_FINISH = 5 # finish video 5 frame early 

def play_video(start_frame = 1, speed = 1, random_flip = True, video_idx = -1, text ="", words_per_line = 8):
    
    video_list = ["joi-1.mp4"] # replace with video or list of videos in directory
   # sample a random video if necessary 
    if(video_idx == -1):
        video_idx = random.randint(0, len(video_list) -1)
    video_file = video_list[video_idx]

    flip = random.randint(0, 1) if random_flip else 0

    if(text != ""):    
        word_list = text.split(" ")
        num_words = len(word_list)
        num_lines = math.ceil(num_words/words_per_line)
        substrings =  [word_list[(i*words_per_line):((i+1)*words_per_line)] for i in range(num_lines)]
    
    cap = cv2.VideoCapture(video_file)
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_count = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame-1)
    cv2.namedWindow("video")
    cv2.moveWindow("video", WINDOW_POSITION[0], WINDOW_POSITION[1])
    
    # main loop to play video
    while(cap.isOpened()):
        ret, frame = cap.read()   
        frame_count+=1
        if(num_frames - start_frame - frame_count<EARLY_FINISH): # cut off last 5 frames
            break
        elif ret:
            frame = cv2.resize(frame, WINDOW_SIZE)
            if flip == 1:
                frame = cv2.flip(frame, 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            if(text != ""):
                #add text to frame
                for idx, s in enumerate(reversed(substrings)):
                    cv2.putText(frame, " ".join(s), 
                                (50, 270 - 15*idx), 
                                font, 0.4, 
                                (0, 255, 255), 
                                1, 
                                cv2.LINE_4)
            # show frame        
            cv2.imshow("video", frame)
            fps = int(BASE_FPS / speed)
            key = cv2.waitKey(fps)
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == 'main':
    play_video()
