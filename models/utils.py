from argparse import ArgumentParser


def get_video_input(input_value):
    if input_value.isnumeric():
        print("카메라 %s 를 입력 장치로 설정합니다...." % input_value)
        return int(input_value)

    print(" '%s' 로부터 입력받는 중......" % input_value)
    return input_value


def add_default_args(parser: ArgumentParser):
    parser.add_argument("--input", type=str, default="0",
                        help="The video input path or video camera id (device id).")

    parser.add_argument("-mdc", "--min-detection-confidence", type=float, default=0.5,
                        help="Minimum confidence value ([0.0, 1.0]) for the detection to be considered successful.")
    parser.add_argument("-mtc", "--min-tracking-confidence", type=float, default=0.5,
                        help=" Minimum confidence value ([0.0, 1.0]) to be considered tracked successfully.")

    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=9001,
                        help="The port the OSC server is listening on")
