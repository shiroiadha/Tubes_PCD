import cv2

def resize_with_aspect_ratio(image, target_width=None, target_height=None):
    h, w = image.shape[:2]
    if target_width is not None:
        scale = target_width / w
        new_w = target_width
        new_h = int(h * scale)
    elif target_height is not None:
        scale = target_height / h
        new_h = target_height
        new_w = int(w * scale)
    else:
        return image

    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)