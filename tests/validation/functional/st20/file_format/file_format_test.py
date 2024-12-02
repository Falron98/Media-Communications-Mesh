# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2024 Intel Corporation
# Intel® Media Communications Mesh

import time
import pytest
import Engine.SenderApp as sender
import Engine.ReceiverApp as receiver

from Engine.execute import call, wait
from Engine.utils import file_format_to_pix_fmt
from Engine.media_files import yuv_files


@pytest.mark.parametrize("file", yuv_files.keys())
def test_st20_file_format(file):
    # sender
    sender_cfg = sender.get_sender_default()
    sender_cfg['file_name'] = yuv_files[file]["filename"]
    sender_cfg['pix_fmt'] = file_format_to_pix_fmt(yuv_files[file]["format"])
    sender_cfg['width'] = yuv_files[file]["width"]
    sender_cfg['height'] = yuv_files[file]["height"]
    sender_cfg['fps'] = yuv_files[file]["fps"]
    sender_cfg['payload_type'] = "st20"
    sender_cmd = sender.get_sender_cmd(sender_cfg)

    # receiver
    receiver_cfg = receiver.get_receiver_st20_cmd()
    receiver_cfg['payload_type'] = "st20"
    receiver_cfg['file_name'] = "test.yuv"
    receiver_cfg['pix_fmt'] = file_format_to_pix_fmt(yuv_files[file]["format"])
    receiver_cfg['width'] = yuv_files[file]["width"]
    receiver_cfg['height'] = yuv_files[file]["height"]
    receiver_cfg['fps'] = yuv_files[file]["fps"]
    receiver_cmd = receiver.get_receiver_cmd(receiver_cfg)

    #media_proxy
    media_proxy_sender = call("sudo media_proxy -d 0000:4b:11.1 -t 9001", "/home/gta/mtl/Media-Communications-Mesh/tests/tools", 25, True)
    media_proxy_receiver = call("sudo media_proxy -d 0000:4b:11.2 -t 9000", "/home/gta/mtl/Media-Communications-Mesh/tests/tools", 25, True)

    time.sleep(5)
    receiver_proc = call(receiver_cmd, "/home/gta/mtl/Media-Communications-Mesh/tests/tools", 15, True)
    sender_proc = call(sender_cmd, "/home/gta/mtl/Media-Communications-Mesh/tests/tools", 15, True)

    wait(media_proxy_sender)
    wait(media_proxy_receiver)
    time.sleep(5)
    wait(receiver_proc)
    wait(sender_proc)

    #TBD: Move test executing to separate file and add result validation

