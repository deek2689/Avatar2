#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import speech_recognition as sr
from rclpy.qos import QoSProfile
from avatar2_interfaces.msg import AudioInput

class ProcessAudioNode(Node):
    def __init__(self):
        super().__init__('audio_source')
        self._msg_id = 0
        self.declare_parameter('topic', '/avatar2/audio_input')
        self._topic = self.get_parameter('topic').get_parameter_value().string_value
        self.declare_parameter('threshold', "0")
        self._threshold = self.get_parameter('threshold').get_parameter_value().double_value
        self.declare_parameter('dynamic', "False")
        self._dynamic = self.get_parameter('dynamic').get_parameter_value().bool_value
        self.declare_parameter('phrase_time_limit', "20.0")
        self._phrase_time_limit = self.get_parameter('phrase_time_limit').get_parameter_value().double_value
        self.declare_parameter('pause_threshold', "0.2")
        self._pause_threshold = self.get_parameter('pause_threshold').get_parameter_value().double_value
        self.declare_parameter('non_speaking_duration', "0.1")
        self._non_speaking_duration = self.get_parameter('non_speaking_duration').get_parameter_value().double_value
        self.declare_parameter('sample_rate', 44100)
        self._sample_rate = self.get_parameter('sample_rate').get_parameter_value().integer_value
        
        self._publisher = self.create_publisher(AudioInput, self._topic, QoSProfile(depth=1))

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = self._pause_threshold
        self.recognizer.non_speaking_duration = self._non_speaking_duration
        self.recognizer.dynamic_energy_threshold = self._dynamic

        if self._threshold > 0:
            self.recognizer.energy_threshold = self._threshold
        else:
            with sr.Microphone(sample_rate=self._sample_rate) as source:
                self.recognizer.adjust_for_ambient_noise(source)

        self.msg_id = 0

        while rclpy.ok():
            with sr.Microphone(sample_rate=self._sample_rate) as source:
                self.get_logger().info(f"Audio source waiting for input {self._phrase_time_limit}")
                if self._phrase_time_limit > 0:
                    audio = self.recognizer.listen(source, phrase_time_limit=self._phrase_time_limit)
                else:
                    audio = self.recognizer.listen(source)

                msg = AudioInput()
                msg.audio = audio.get_wav_data().hex()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.seq = self._msg_id
                self._msg_id = self._msg_id + 1
                self._publisher.publish(msg)
                self.get_logger().info(f"Audio source sent {len(msg.audio)} samples")

def main(args=None):
    rclpy.init(args=args)
    node = ProcessAudioNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
