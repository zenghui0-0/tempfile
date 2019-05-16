"""
@summary:   (Android only)Repeatedly play an audio file for the specified amount of time, using the low-level ALSA audio player.
            ALSA is unique to Linux/Android, so this does not apply to other OSes.
            PREREQUISITES:
            The following files must be installed in the /system/bin directory on the DUT:
                /system/bin/alsa_amixer
                /system/bin/alsa_aplay
            The contents of audio_playback_alsa_scripts.tgz must be unpacked in the directory specified by SCRIPTS_PATH.
                This tarball can be found in Artifactory at acs_test_artifacts/CONCURRENCY/TESTS/audio_playback_alsa/audio_playback_alsa_scripts.tgz
            This audio file must be installed on the DUT:
                /sdcard/Music/s_48k_16.wav.
                It can be found in Artifactory at acs_test_artifacts/CONCURRENCY/AUDIO/s_48k_16.wav.
@since 8 August 2014
@author: Stephen A Smith
@organization: INTEL PEG-SVE-DSV

@copyright: (c)Copyright 2014, Intel Corporation All Rights Reserved.
The source code contained or described here in and all documents related
to the source code ("Material") are owned by Intel Corporation or its
suppliers or licensors. Title to the Material remains with Intel Corporation
or its suppliers and licensors. The Material contains trade secrets and
proprietary and confidential information of Intel or its suppliers and
licensors.

The Material is protected by worldwide copyright and trade secret laws and
treaty provisions. No part of the Material may be used, copied, reproduced,
modified, published, uploaded, posted, transmitted, distributed, or disclosed
in any way without Intel's prior express written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be expressed
and approved by Intel in writing.
"""

from Core.TestStep.DeviceTestStepBase import DeviceTestStepBase
from ErrorHandling.DeviceException import DeviceException
from UtilitiesFWK.Utilities import Global

class PlayAudioAlsaLoop(DeviceTestStepBase):
    def run(self, context):
        """
        Runs the test step
        @type context: TestStepContext
        @param context: test case context
        """
        DeviceTestStepBase.run(self, context)
        self._logger.info(self._pars.id + ": Run")
        self.system_api = self._device.get_uecmd("System")
        self.file_api = self._device.get_uecmd("File")

        basename = "loopAudioPlaybackAlsa"
        #To make this OS-independent, look for different possible filenames.
        #If anyone enables this in Windows, I assume they will create a DOS batch file to do what loopAudioPlaybackAlsa.sh does.
        #Add to this list if required for any other OS.
        possible_extensions = [".sh", ".bat"]
        for ext in possible_extensions:
            #uecmd or underlying code should take care of changing path delimiters as needed
            script = self._pars.scripts_path + self._device.get_device_os_path().sep + basename + ext
            found = self.file_api.exist(script)
            if found:
                break
        if not found:
            msg = self._pars.id + ": Could not find a " + basename + ".* script."
            self._logger.error(msg)
            raise DeviceException(DeviceException.OPERATION_FAILED, msg)

        args = '%d %d'%(self._pars.duration,self._pars.use_headphones)
        """Adding a extra small amount of time to the timeout, in case something goes a little long"""
        """run_shell_executable doesn't return anything, but will raise an exception if it fails"""
        self.system_api.run_shell_executable(script, args, io_redirection=2, timeout=self._pars.duration*60 + 120)
        self._logger.info(self._pars.id + ": Done")
