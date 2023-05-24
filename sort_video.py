#Import libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def load_matrices(file_path: str):
    matrix=np.load(f"./frames_npy/frame0{file_path}_pixels.npy")
    return matrix.reshape(720,1280)
def plot_image(matrix):
    plt.imshow(matrix, cmap='gray')
    plt.axis('off')
    plt.show()


def MSE(matrix1,matrix2):
    error=0.0
    x,y=len(matrix1),len(matrix1[0])
    for i in range(x):
        for j in range(y):
            error+=(matrix1[i,j]-matrix2[i,j])**2
    return error/(x*y)


def L1_error(matrix1,matrix2):
    error=0.0
    x,y=len(matrix1),len(matrix1[0])
    for i in range(x):
        for j in range(y):
            error+=np.abs(matrix1[i,j]-matrix2[i,j])
    return error/(x*y)


def make_video(frame_dir: str, output_path:str, fps:int):

    # Get the frame dimensions from the first frame
    frame_path = os.path.join(frame_dir, os.listdir(frame_dir)[0])
    frame = cv2.imread(frame_path)
    frame_height, frame_width, _ = frame.shape

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Specify the video codec
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        # Write the frames to the video
    frame_files = sorted(
        [file for file in os.listdir(frame_dir) if file.endswith('.jpg') and file.startswith('frame')],
        key=lambda x: int(x[5:-4])
    )
    for frame_file in frame_files:
        frame_path = os.path.join(frame_dir, frame_file)
        frame = cv2.imread(frame_path)
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()



video=[]                    #unsorted frames list
n_frames=100                #number of frames
for i in range(0,n_frames): #load frames from files
    if i <=9:
        video.append(load_matrices(f"0{i}"))
    else:
        video.append(load_matrices(f"{i}"))


sort_video=[]               #sorted frames list
sort_video.append(video[0]) #first frame is the first chronologically
used_indexes=[0,]           


for _ in range(len(video)):  #Main Loop
    error_list=[]
    if _ ==0: 
        min_index=0
        plt.imsave(f"./frames_sorted/frame{_}.jpg",sort_video[min_index],cmap='gray')

    for j, frame2 in enumerate(video):
        print(j,min_index,used_indexes)
        if j==min_index or j in used_indexes:
            error_list.append(np.Infinity)
        else:
            error_list.append(L1_error(video[min_index],video[j]))

    #Retrieve the index of the lowest error in the list
    min_index=np.argmin(error_list)
    # Append this frame to the sorted video list, just in case
    sort_video.append(video[min_index])
    #Append this index to the used_indexes list
    used_indexes.append(min_index)
    #save fig in sorted frames folder
    plt.imsave(f"./frames_sorted/frame{_}.jpg",sort_video[-1],cmap='gray')

#Make video
frames_folder_path="./frames_sorted"
video_ouput_path="./frames_sorted/reconstructed_video.mp4"
fps=30
make_video(frames_folder_path,video_ouput_path,fps)
















