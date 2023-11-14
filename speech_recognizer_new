#!/usr/bin/env python3


# all the above imports are for Ros2
import rclpy
from rclpy.node import Node
import speech_recognition as sr
from rclpy.qos import QoSProfile
from avatar2_interfaces.msg import AudioInput   # based on the message import the messages from the avater2_interface 
from avatar2_interfaces.msg import TaggedString

# Do speech recognition based on a custom trained PocketSphinx model
#
import rospy
import rospkg
import io
import os
import speech_recognition as sr
from sentrybot_msgs.msg import AudioInput
from sentrybot_msgs.msg import TaggedString
from std_msgs.msg import String

class Recognizer(Node):
    def __init__(self):
        super().__init__('speech_recognizer')
        self._msg_id = 0
        self.declare_parameter("~root", rospkg.RosPack().get_path("sentrybot_audio"))
        self._lmfile = self.get_parameter('dynamic').get_parameter_value().bool_value
        self._sr_loc = sr.__path__[0]
        self.declare_parameter("~lm", "pocketsphinx_model/test_cmd.lm")
        self._lmfile = self.get_parameter('lmfile')
        self._lm = os.path.join(root, self._lmfile)
        self._hmm = os.path.join(sr_loc,  "pocketsphinx-data/en-US/acoustic-model")
        self._dict = os.path.join(sr_loc, "pocketsphinx-data/en-US/pronounciation-dictionary.dict")
        self._subscription = self.create_subscription(source_topic, AudioInput, self._callback)
        self._publisher = self.create_publisher(destination_topic, TaggedString, queue_size=10)
        self._recognizer = sr.Recognizer()
        self._language = language
        self._recognizer.pause_threshold = self._pause_threshold
        self._recognizer.non_speaking_duration = self._non_speaking_duration
        self._recognizer.dynamic_energy_threshold = self._dynamic
        
        self.get_logger().info(f" {rospy.get_caller_id()} callback")
        wav_img = sr.AudioFile(io.BytesIO(bytes.fromhex(data.audio)))
        with wav_img as source:
            audio = self._recognizer.record(source)
           try:
            z = self._recognizer.recognize_sphinx(audio, language=self._language)
            msg = TaggedString()
            msg.header.stamp = rospy.Time.now()
            msg.header.seq = self._msg_id
            msg.audio_sequence_number = data.header.seq
            msg.text = String()
            msg.text.data = z
            self._msg_id = self._msg_id + 1
            self._publisher.publish(msg)
        except sr.UnknownValueError:
             z = "??"
        self.get_logger().info(f" {rospy.get_caller_id()} heard >{z}<")


def main(args=None):
    rclpy.init(args=args)
    node = Recognizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
