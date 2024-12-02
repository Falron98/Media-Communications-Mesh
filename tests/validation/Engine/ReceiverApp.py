# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2024 Intel Corporation
# Intel® Media Communications Mesh

import os


def get_receiver_default(app_path = "/home/gta/mtl/Media-Communications-Mesh/tests/tools/recver_val") -> dict:
    return {
        "media_proxy_port": 9002,
        "app_path": app_path,
        "file_name": "input.yuv",
        "width": 1920,
        "height": 1080,
        "fps": 25,
        "pix_fmt": "yuv422p10le",
        "recv_ip": "192.168.2.1",
        "recv_port": 9002,
        "send_ip": "192.168.2.2",
        "send_port": 9001,
        "protocol_type": "auto",
        "payload_type": "st20",
        "socketpath": "/run/mcm/mcm_rx_memif.sock",
        "interfaceid": 0,
        "loop": 0,
    }


def get_receiver_cmd(config: dict) -> str:
    return """sudo MCM_MEDIA_PROXY_PORT={media_proxy_port} \
    {app_path} \
    -w {width} \
    -h {height} \
    -f {fps} \
    -x {pix_fmt} \
    -s {send_ip} \
    -p {send_port} \
    -r {recv_ip} \
    -i {recv_port} \
    -b {file_name}
    """.format(**config)

def get_receiver_st20_cmd(config: dict) -> str:
    return """sudo MCM_MEDIA_PROXY_PORT={media_proxy_port} \
    {app_path} \
    -w {width} \
    -h {height} \
    -f {fps} \
    -x {pix_fmt} \
    -s {send_ip} \
    -p {send_port} \
    -b {file_name}
    """.format(**config)
