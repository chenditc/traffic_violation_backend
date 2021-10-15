from __future__ import print_function

import os
import time

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

from .data import cfg_mnet
from .layers.functions.prior_box import PriorBox
from .models.retina import Retina
from .utils.box_utils import decode, decode_landm
from .utils.nms.py_cpu_nms import py_cpu_nms

import pathlib
curr_path = pathlib.Path(__file__).parent.resolve()

class PlateDetect:

    def __init__(self, confidence_threshold=0.5, top_k=2000, keep_top_k=1000, nms_threshold=0.4):
        torch.set_grad_enabled(False)
        cfg = cfg_mnet
        net = Retina(cfg=cfg, phase='test')
        net = self.load_model(net, str(curr_path) + '/weights/mnet_plate.pth', True)
        net.eval()
        print('Finished loading model!')

        cudnn.benchmark = True
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.cfg = cfg_mnet
        self.device = device
        self.net = net.to(device)

        self.confidence_threshold = confidence_threshold
        self.top_k = top_k
        self.keep_top_k = keep_top_k
        self.nms_threshold = nms_threshold

    def check_keys(self, model, pretrained_state_dict):
        ckpt_keys = set(pretrained_state_dict.keys())
        model_keys = set(model.state_dict().keys())
        used_pretrained_keys = model_keys & ckpt_keys
        unused_pretrained_keys = ckpt_keys - model_keys
        missing_keys = model_keys - ckpt_keys
        print('Missing keys:{}'.format(len(missing_keys)))
        print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
        print('Used keys:{}'.format(len(used_pretrained_keys)))
        assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
        return True

    def remove_prefix(self, state_dict, prefix):
        ''' Old style model is stored with all names of parameters sharing common prefix 'module.' '''
        print('remove prefix \'{}\''.format(prefix))
        f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
        return {f(key): value for key, value in state_dict.items()}

    def load_model(self, model, pretrained_path, load_to_cpu):
        print('Loading pretrained model from {}'.format(pretrained_path))
        if load_to_cpu:
            pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
        else:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage.cuda(device))
        if "state_dict" in pretrained_dict.keys():
            pretrained_dict = self.remove_prefix(pretrained_dict['state_dict'], 'module.')
        else:
            pretrained_dict = self.remove_prefix(pretrained_dict, 'module.')
        self.check_keys(model, pretrained_dict)
        model.load_state_dict(pretrained_dict, strict=False)
        return model

    def show_files(self, path, all_files):
        # 首先遍历当前目录所有文件及文件夹
        file_list = os.listdir(path)
        # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
        for file in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
            cur_path = os.path.join(path, file)
            # 判断是否是文件夹
            if os.path.isdir(cur_path):
                self.show_files(cur_path, all_files)
            else:
                if cur_path.find(".jpg") > 0:
                    all_files.append(cur_path)

        return all_files

    def detect(self, num, image):
        img = np.float32(image)

        im_height, im_width, _ = img.shape
        scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
        img -= (104, 117, 123)
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.to(self.device)
        scale = scale.to(self.device)

        tic = time.time()
        loc, conf, landms = self.net(img)  # forward pass
        print('net forward time: {:.4f}'.format(time.time() - tic))

        priorbox = PriorBox(self.cfg, image_size=(im_height, im_width))
        priors = priorbox.forward()
        priors = priors.to(self.device)
        prior_data = priors.data
        boxes = decode(loc.data.squeeze(0), prior_data, self.cfg['variance'])
        boxes = boxes * scale
        boxes = boxes.cpu().numpy()

        scores = conf.squeeze(0).data.cpu().numpy()[:, 1]

        landms = decode_landm(landms.data.squeeze(0), prior_data, self.cfg['variance'])
        scale1 = torch.Tensor([img.shape[3], img.shape[2], img.shape[3], img.shape[2],
                               img.shape[3], img.shape[2],
                               img.shape[3], img.shape[2]])
        scale1 = scale1.to(self.device)
        landms = landms * scale1
        landms = landms.cpu().numpy()

        # ignore low scores
        inds = np.where(scores > self.confidence_threshold)[0]
        boxes = boxes[inds]
        landms = landms[inds]
        scores = scores[inds]

        # keep top-K before NMS
        order = scores.argsort()[::-1][:self.top_k]
        boxes = boxes[order]
        landms = landms[order]
        scores = scores[order]

        # do NMS
        dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
        keep = py_cpu_nms(dets, self.nms_threshold)
        dets = dets[keep, :]
        landms = landms[keep]

        # keep top-K faster NMS
        dets = dets[:self.keep_top_k, :]
        landms = landms[:self.keep_top_k, :]

        dets = np.concatenate((dets, landms), axis=1)
        print('priorBox time: {:.4f}'.format(time.time() - tic))

        # for b in dets:
        #     b = list(map(int, b))
        #     cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 5)
        # cv2.imwrite(f"imgs/{num}.jpg", image)

        return [x[:4] for x in dets]
