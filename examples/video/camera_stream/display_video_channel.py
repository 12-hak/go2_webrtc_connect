import asyncio
import logging
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaRecorder


# Enable logging for debugging
logging.basicConfig(level=logging.FATAL)

# Define the output video file and format
output_filename = 'output_video.mp4'

# Initialize the MediaRecorder instance
recorder = MediaRecorder(output_filename)

# Function to handle receiving video frames and recording them
async def recv_camera_stream(track: MediaStreamTrack):
    while True:
        print("Frame")
        frame = await track.recv()
        # Process the video frame, e.g., display using OpenCV
        img = frame.to_ndarray(format="bgr24")

        print(f"Shape: {img.shape}, Dimensions: {img.ndim}, Type: {img.dtype}, Size: {img.size}")

        #ToDo: add opencv output to window. For some reason it doesnt work as expected

  

# Main function for setting up the WebRTC connection and handling streams
async def main():
    try:
        # Choose a connection method (uncomment the correct one)
        conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.8.181")
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.Remote, serialNumber="B42D2000XXXXXXXX", username="email@gmail.com", password="pass")
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)

        # Connect to the device
        await conn.connect()

        # Switch video channel on and start receiving video frames
        conn.video.switchVideoChannel(True)

        # Add callback to handle received video frames (track)
        conn.video.add_track_callback(lambda track: asyncio.create_task(recv_camera_stream(track)))

        # Keep the program running while recording
        await asyncio.sleep(20)  # Run for 20 seconds or adjust as needed

    except ValueError as e:
        logging.error(f"Error in WebRTC connection: {e}")

    finally:
        # Ensure that the recorder is properly stopped and closed
        await recorder.stop()

if __name__ == "__main__":
    asyncio.run(main())