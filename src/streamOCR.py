import difflib
import pytesseract
import numpy as np
import subprocess
import json
import cv2

class VideoOCR:
    def __init__(self, urls):
        self.urls = urls
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def get_video_resolution(self, url):  # 영상 fps, 프레임 가져오기
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate',
            '-of', 'json',
            url
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception("Failed to get video resolution")
        info = json.loads(result.stdout)
        width = info['streams'][0]['width']
        height = info['streams'][0]['height']
        r_frame_rate = info['streams'][0]['r_frame_rate']
        numerator, denominator = map(int, r_frame_rate.split('/'))
        fps = numerator / denominator if denominator != 0 else 0
        return width, height, fps

    def detect_significant_change(self, current_frame, prev_frame, threshold=50000):
        diff = cv2.absdiff(current_frame, prev_frame)
        return np.sum(diff) > threshold

    def enhanced_ocr(self, frame):
        config = '-l eng --oem 3 --psm 6 -c preserve_interword_spaces=1'
        return pytesseract.image_to_string(frame, config=config)

    def text_similarity(self, text1, text2):
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def save_results(self, detected_texts, output_file='extracted_data.json'):
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(detected_texts, file, indent=4, ensure_ascii=False)

    def process_video(self, video_index, frame_sampling_rate=100, similarity_threshold=0.23):
        ffmpeg_command = [
            'ffmpeg',
            '-i', self.urls[video_index],
            '-loglevel', 'quiet', # 로그 출력 x
            '-an', # 오디오 스트림 무시
            '-f', 'image2pipe', # 비디오 파이프라인 설정
            '-pix_fmt', 'bgr24', # color 포멧 변경
            '-vcodec', 'rawvideo', # 비디오 코덱 설정
            '-'

        ]
        pipe = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)
        width, height, fps = self.get_video_resolution(self.urls[video_index])
        frame_size = width * height * 3
        detected_texts = []
        prev_frame = None
        frame_count = 0
        current_text = ""
        start_time = None


        while True:
            raw_frame = pipe.stdout.read(frame_size)


            if not raw_frame:
                print("끝")
                break
            frame = np.frombuffer(raw_frame, dtype='uint8').reshape((height, width, 3))

            cv2.imshow("video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if frame_count % frame_sampling_rate == 0 and prev_frame is not None:
                if self.detect_significant_change(frame, prev_frame, 50000):
                    text = self.enhanced_ocr(frame)
                    print(text)
                    if text.strip() and (not current_text or self.text_similarity(text, current_text) < similarity_threshold):
                        if current_text:
                            detected_texts.append({
                                "start_timestamp": start_time,
                                "end_timestamp": frame_count / fps,
                                "text": current_text
                            })
                        current_text = text
                        start_time = frame_count / fps
                prev_frame = frame
            else:
                prev_frame = frame

            frame_count += 1

        if current_text:
            detected_texts.append({
                "start_timestamp": start_time,
                "end_timestamp": frame_count / fps,
                "text": current_text
            })


        cv2.destroyAllWindows()
        pipe.terminate()
        self.save_results(detected_texts, 'video_ocr.json')



if __name__ == "__main__":
    urls = [
        "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4",
        "https://another-url.com/video.mp4"
    ]
    ocr_processor = VideoOCR(urls)
    ocr_processor.process_video(0)