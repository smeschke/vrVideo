import cv2
import numpy as np

# === INPUT VIDEO ===
cap = cv2.VideoCapture('/home/smeschke/Desktop/rival/rivalTrimmed_sbs_2880x2880.mp4')

# === CONFIGURATION ===
HSV_LOWER = np.array([35, 25, 155])   # Green ball
HSV_UPPER = np.array([81, 255, 255])

# === VIDEO PROPERTIES ===
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 90

# === OUTPUT VIDEO ===
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/home/smeschke/Desktop/rival/overlay.mp4', fourcc, fps, (frame_width, frame_height))

# === INITIALIZE 'PAINT' CANVAS ===
paint = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
#paint = np.zeros((1234, 2345, 3), dtype=np.uint8)
hue = 0

def get_bgr_from_hue(h):
    hsv_color = np.uint8([[[h, 255, 255]]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    return tuple(int(c) for c in bgr_color)

# === MAIN LOOP ===
while True:
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (2345,1234))
    if not ret:
        break

    # === SEGMENT GREEN ===
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)

    # === MAKE MASK INTO COLORED REGION ===
    color = get_bgr_from_hue(hue)
    hue = (hue + .05) % 180  # wrap hue between 0–179

    color_img = np.full_like(frame, color)
    colored_mask = cv2.bitwise_and(color_img, color_img, mask=mask)

    # === ADD COLORED MASK TO PAINT IMAGE ===
    #paint = cv2.add(paint, colored_mask)  # adds new color over old
    # Create inverse mask to keep old paint where new mask is zero
    inverse_mask = cv2.bitwise_not(mask)
    inverse_mask_3ch = cv2.merge([inverse_mask] * 3)

    # Keep old paint where mask is not active
    paint_bg = cv2.bitwise_and(paint, inverse_mask_3ch)

    # Add new hue where mask is active
    paint_fg = cv2.bitwise_and(colored_mask, colored_mask, mask=mask)

    # Combine both
    paint = cv2.add(paint_bg, paint_fg)


    # === OVERLAY PAINT ON ORIGINAL FRAME ===
    paint_gray = cv2.cvtColor(paint, cv2.COLOR_BGR2GRAY)
    mask_paint = cv2.threshold(paint_gray, 1, 255, cv2.THRESH_BINARY)[1]
    inv_mask = cv2.bitwise_not(mask_paint)

    background = cv2.bitwise_and(frame, frame, mask=inv_mask)
    final_frame = cv2.add(background, paint)

    # === DISPLAY + SAVE ===
    cv2.imshow("Paint Overlay", final_frame)
    out.write(final_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# === CLEANUP ===
cap.release()
out.release()
cv2.destroyAllWindows()
