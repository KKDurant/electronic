import os
import sys
from pathlib import Path
import numpy as np
import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 根目录
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # 相对路径

from models.common import DetectMultiBackend
from utils.general import ( check_img_size,  cv2, non_max_suppression, scale_coords)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
from utils.augmentations import letterbox

class YoloModel:
    @torch.no_grad()#停止autograd模块的工作
    def __init__(self,
            weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
            data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
            imgsz=(640, 640),  # inference size (height, width)
            conf_thres=0.5,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            hide_labels=False,  # hide labels
            hide_conf=False,  # hide confidences
            half=False,  # use FP16 half-precision inference
    ) -> None:#初始化，加载模型

        self.save_img= True
        
        # Load model
        #self.device = select_device(device)
        self.device= torch.device('cpu')
        self.model = DetectMultiBackend(weights, device=self.device, data=data, fp16=half)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        
        # NMS相关参数
        self.conf_thres=conf_thres
        self.iou_thres=iou_thres
        self.max_det=max_det
        self.augment=augment
        self.classes=classes
        self.agnostic_nms=agnostic_nms
        
        # 显示相关参数设定
        self.hide_conf=hide_conf
        self.hide_labels=hide_labels
        pass
    @torch.no_grad()#停止autograd模块的工作
    def run(self,imBGR):

        # Padded resize
        img = letterbox(imBGR, self.imgsz, stride=self.stride, auto=self.pt)[0]

        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        
        # Run inference
        self.model.warmup(imgsz=(1, 3, *self.imgsz))  # warmup
        im = torch.from_numpy(img).to(self.device)
        im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        #names = self.model.module.names if hasattr(self.model, 'module') else self.model.names

        # Inference
        pred = self.model(im, augment=self.augment, visualize=False)

        # NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            im0 = imBGR.copy()
            annotator = Annotator(im0, line_width=3, example=str(self.names))
            obj_detected=[]
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    #if self.save_img:  # Add bbox to image
                    c = int(cls)  # integer class
                    label = None if self.hide_labels else (self.names[c] if self.hide_conf else f'{self.names[c]} {conf:.2f}')
                    #label=self.names[c]
                    annotator.box_label(xyxy, label, color=colors(c, True))
                    content_dict = {
                        #"name": file_name[len(file_name)-1],
                        #"category": (names[int(cls)]),
                        "category":label,
                        "bbox": torch.tensor(xyxy).view(1, 4).view(-1).tolist(),
                        "score": conf.tolist()
                    }
                    obj_detected.append(content_dict)
            im0 = annotator.result()
            return im0,obj_detected

if __name__ == "__main__":
    yolomodel=YoloModel(weights=ROOT /"bestm_tr.pt",data=ROOT /"LEDDetection_m_tr.yaml")
    imBGR= cv2.imread(ROOT /"A10-1.jpg")
    yolomodel.run(imBGR)
    #imBGR= cv2.imread("./A1-2.jpg")
    #yolomodel.run(imBGR)