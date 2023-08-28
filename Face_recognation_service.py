import face_recognition
import numpy as np
import cv2


# векторные представления лиц, имена, user_id в БД
known_face_encodings, known_face_names, known_face_uids = [], [], []

def run_rec():
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while video_capture.isOpened():
        # чтение кадра с камеры
        ret, frame = video_capture.read()
        # уменьшение разрешения (для быстродействия)
        divideint = 2
        small_frame = cv2.resize(frame, (0, 0), fx=1 / divideint, fy=1 / divideint)
        # уменьшение размерности матрицы изображения, аналог [:, :, ::-1] 
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # обрабатывается каждый 3й кадр (для быстродействия)
        if process_this_frame % 3 == 0:
            # расположение лиц
            face_locations = face_recognition.face_locations(rgb_small_frame)
            # преобразование лиц в векторы
            face_encodings = face_recognition.face_encodings(rgb_small_frame, 
  face_locations)
            # сравнение обнаруженных лиц с лицами в базе
            for face_encoding in face_encodings:
                name = "Unknown"
                # вычисление векторного расстояния (мера схожести векторов)
                # known_face_encodings - 
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                # определение индекса максимально похожего лица
                best_match_index = np.argmin(face_distances)
                # проверка на степень похожести 
                # похожи если векторное расстояние расстояние меньше 0.6
                if face_distances[best_match_index] < 0.6:
                    # имя обнаруженного лица для пользователя
                    name = known_face_names[best_match_index]
                    # user_id лица для внутреннего использования
                    uid = known_face_uids[best_match_index]


def get_db():
    conn = sqlite3.connect("face_db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM FRS")
    facecount = cursor.fetchall()

    known_face_encodings = []
    known_face_names = []
    known_face_uids = []
    face_in_home = []

    for i in range(len(facecount)):
        a = pickle.loads(facecount[i][5])
        known_face_encodings.append(a)
        known_face_names.append(facecount[i][1])
        known_face_uids.append(facecount[i][0])
        face_in_home.append(facecount[i][10])

    return known_face_encodings,
    known_face_names,
    known_face_uids,
    face_in_home, conn


# запуск камеры
video_capture = cv2.video_capture(0, cx2.CAP_DSHOW)

# изменение размеров и имени окна для показа изображения
video_capture.set(3, 800)
video_capture.set(4, 448)
сv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 800, 448)

# расположение краев прямоугольника, обозначающего лицо в кадре; имя
for (top, right, bottom, left), name in zip(face_locations, face_names):
    # рисуем прямоугольник вокруг лица
    cv2.rectangle(frame, (left, top), (right, bottom), (107, 168, 0), 2)

    # рисует плашку под текст с именем пользователя
    cv2.rectangle(frame, (left, bottom - 23), (right, bottom), (107, 168, 0), cv2.FILLED)
    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_ITALIC, 0.5, (0, 0, 0), 1)

    # отображение состояния системы
    cv2.rectangle(frame, (8, 5), (228, 64), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, 'RECOGNITION IN PROGRESS', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
    cv2.putText(frame, 'Model: face-recognition', (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)