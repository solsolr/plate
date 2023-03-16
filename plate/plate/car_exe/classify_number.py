from .header import plate_preprocess
from .header import plate_candidate
from .header import plate_classify
from ..forms import CarForm
import numpy as np, cv2

def start(car_no):
    image, morph = plate_preprocess.preprocessing(car_no) # 전처리
    # image = cv2.resize(image, dsize=(600, 400), interpolation=cv2.INTER_AREA)
    # morph = cv2.resize(morph, dsize=(600, 400), interpolation=cv2.INTER_AREA)
    candidates = plate_preprocess.find_candidates(morph)  # 후보 영역 검색

    fills = [plate_candidate.color_candidate_img(image, size) for size, _, _ in candidates]
    new_candis = [plate_preprocess.find_candidates(fill) for fill in fills]
    new_candis = [cand[0] for cand in new_candis if cand]
    candidate_imgs = [plate_candidate.rotate_plate(image, cand) for cand in new_candis]

    svm = cv2.ml.SVM_load("plate/car_exe/SVMtrain.xml")                  # 학습된 데이터 적재
    rows = np.reshape(candidate_imgs, (len(candidate_imgs), -1))    # 1행 데이터들로 변환
    _, results = svm.predict(rows.astype("float32"))                # 분류 수행
    result = np.where(results == 1)[0]        # 1인 값의 위치 찾기

    plate_no = result[0] if len(result)>0 else -1

    K1, K2 = 10, 10
    nknn = plate_classify.kNN_train("plate/car_exe/images/train_numbers.png", K1, 10, 20) # 숫자 학습
    tknn = plate_classify.kNN_train("plate/car_exe/images/train_texts.png", K2, 40, 20)   # 문자 학습

    if plate_no >= 0:
        plate_img = plate_classify.preprocessing_plate(candidate_imgs[plate_no])   # 번호판 영상 전처리
        cells_roi = plate_classify.find_objects(cv2.bitwise_not(plate_img))
        cells = [plate_img[y:y+h, x:x+w] for x,y,w,h in cells_roi]

        plate_classify.classify_numbers(cells, nknn, tknn, K1, K2, cells_roi)      # 숫자 객체 분류
        pts = np.int32(cv2.boxPoints(new_candis[plate_no]))
        cv2.polylines(image, [pts], True,  (0, 255, 0), 2)

        color_plate = cv2.cvtColor(plate_img, cv2.COLOR_GRAY2BGR)  # 컬러 번호판 영상

        for x,y, w, h in cells_roi:
            cv2.rectangle(color_plate, (x,y), (x+w,y+h), (0, 0, 255), 1)        # 번호판에 사각형 그리기
        h,w  = color_plate.shape[:2]
        image[0:h, 0:w] = color_plate
    else:
        print("번호판 미검출")
    src = "media/images/r_%s" %car_no
    cv2.imwrite(src, image)
    return image