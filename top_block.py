#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Nov 19 13:53:59 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import sip
import sys
import threading
import time
import random
from gnuradio import qtgui
class top_block(gr.top_block, Qt.QWidget):
    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.samp_rate = samp_rate = 10e6
        self.center_freq = center_freq = 0
        ##################################################
        # Blocks
        ##################################################
        self.probe = blocks.probe_signal_f()
        self._center_freq_tool_bar = Qt.QToolBar(self)
        self._center_freq_tool_bar.addWidget(Qt.QLabel("center_freq"+": "))
        self._center_freq_line_edit = Qt.QLineEdit(str(self.center_freq))
        self._center_freq_tool_bar.addWidget(self._center_freq_line_edit)
        self._center_freq_line_edit.returnPressed.connect(
        lambda:
        self.set_center_freq(int(str(self._center_freq_line_edit.text().toAscii())
        )))
        self.top_grid_layout.addWidget(self._center_freq_tool_bar)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")), # addr=192.168.50.2
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(200, 0) #gain of Jammer
        self.digital_ofdm_mod_0 = grc_blks2.packet_mod_c(digital.ofdm_mod(
            options=grc_blks2.options(
                    modulation="qpsk",
                    fft_length=4096,
                #    occupied_tones=60,#Frequency BW
                    occupied_tones=60,
                    cp_length=128,
                    pad_for_usrp=True,
                    log=None,
                    verbose=None,
                ),
            ),
            payload_length=16,
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1,samp_rate,True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate,analog.GR_COS_WAVE, 1000, 1, 0)
#        self.Clock = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE,20, 1, 0)
        self.Clock = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE,.5, 1, 0)

        def _variable_function_probe_0_probe():
            while True:
                val = self.probe.level()
                if val ==0:
                    # self.set_center_freq(random.randrange(5.915e9,5.917e9,1e3))
                #    self.set_center_freq(5.9165e9)
                #    self.set_center_freq([5.915e9,5.916e9,5.917e9][random.randint(0,2)])#random.randrange(2.6775e9,2.6825e9,1e3)) # work on specifying set of non-random frequencies 
                    # want to jam on certain frequencies for 1.5 seconds
                    self.set_center_freq(random.randrange(5.9165e9,5.917e9,1e3))
                try:
                    self.set_variable_function_probe_0(val)
                except AttributeError:
                    pass
             #   time.sleep(1.0 / (40)) # change denominator to be smaller so jamming refresh rate is bigger
                time.sleep(1.0/(1.0))
                # consider activating jammer on condition from an SNR block

        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.Clock, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.digital_ofdm_mod_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.probe, 0))
        self.connect((self.digital_ofdm_mod_0, 0), (self.uhd_usrp_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.Clock.set_sampling_freq(self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        Qt.QMetaObject.invokeMethod(self._center_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.center_freq)))
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)

def main(top_block_cls=top_block, options=None):
    from distutils.version import StrictVersion
    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)
    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
