import face_recognition as fr
import cv2
import os

from func import f_addVideotodb


class Video:
    def __init__(self):
        self.flag_recording = False
        self.number_recording = 0

    def run(self):
        self.cap = cv2.VideoCapture('../test_media/a.mp4')
        known_people = os.listdir('../people')

        self.start_recording()

        while self.cap.isOpened():
            try:
                success, self.img = self.cap.read()
                if not success:
                    if self.flag_recording:
                        self.stop_recording()
                    break

                cv2.imwrite('../photo/image.jpeg', self.img)

                img_fr = fr.load_image_file('../photo/image.jpeg')
                faces_loc = fr.face_locations(img_fr)
                find_fasec = len(faces_loc)

                for i in range(find_fasec):

                    y, x1, y1, x = faces_loc[i]
                    cv2.imwrite('../photo/image_face.jpeg', self.img[y:y1, x:x1])
                    cv2.rectangle(self.img, (x, y), (x1, y1), (250, 250, 0), 2)
                    result = False

                    for i_face in known_people:
                        known_face = fr.load_image_file(f'../people/{i_face}')
                        known_face_enc = fr.face_encodings(known_face)[0]

                        unknown_face = fr.load_image_file('../photo/image_face.jpeg')
                        unknown_face_enc = fr.face_encodings(unknown_face)[0]

                        result = fr.compare_faces([known_face_enc], unknown_face_enc)

                        if result:
                            name = i_face[:i_face.find('.')].split('_')[0]
                            surname = i_face[:i_face.find('.')].split('_')[1]
                            cv2.putText(self.img, f"{name} {surname}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (20, 20, 0), 2,
                                        cv2.LINE_AA)
                            if self.flag_recording:
                                self.sp_peoples.add(f"{name} {surname}")
                            break

                    if not result:
                        cv2.putText(self.img, 'unknown', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 0), 1,
                                    cv2.LINE_AA)
                        if self.flag_recording:
                            self.count_not_known += 1

                cv2.imwrite('../photo/image_2.jpeg', self.img)

                if self.flag_recording:
                    self.video_recording.write(self.img)

            except Exception:
                pass

    def start_recording(self):
        self.sp_peoples = set()
        self.count_not_known = 0
        self.flag_recording = True
        self.number_recording += 1
        # self.dt_rec = self.dateTimeEd.dateTime()

        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        self.video_recording = cv2.VideoWriter(f'../recording_video/recording_{self.number_recording}.avi', fourcc,
                                               20.0, (frame_width, frame_height))

    def stop_recording(self):
        self.flag_recording = False
        f_addVideotodb(1, self.sp_peoples, self.count_not_known,
                       f'../recording_video/recording_{self.number_recording}.avi')


a = Video()
a.run()
