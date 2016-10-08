"""test tts module."""
import random
import string
import unittest
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

try:
    from melissa.tts import tts
except IOError:
    # NOTE: don't test with existing profile.
    # taken from http://stackoverflow.com/a/8658332
    # mocking the import so mock_profile could be loaded.
    # Store original __import__
    orig_import = __import__
    # This will be the profile module
    mock_profile = mock.Mock()
    # set mock as default value to make run the test
    DEFAULT_PROFILE_DATA = {
        'va_gender': mock.Mock(),
        'tts': mock.Mock(),
    }
    mock_profile.data = DEFAULT_PROFILE_DATA

    # mock_import side effect
    def import_mock(name, *args):
        """import mock side effect."""
        if name == 'profile':
            return mock_profile
        return orig_import(name, *args)

    with mock.patch('__builtin__.__import__', side_effect=import_mock):
        from melissa.tts import tts


def get_random_string(exclude_list):
    """get random gender which is not 'female' or 'male'."""
    length = 10
    result = ''.join(random.choice(string.lowercase) for i in range(length))
    while result in exclude_list:
        result = ''.join(
            random.choice(string.lowercase) for i in range(length)
        )
    return result


def test_empty_string():
    """test empty string."""
    assert tts('') == 0


def test_mock_input():
    """test using different type of variable such as Mock object."""
    # NOTE: tts only receive string or equivalent as input.
    with pytest.raises(TypeError):
        tts(mock.Mock())


@mock.patch('melissa.tts.subprocess')
@mock.patch('melissa.tts.sys')
class TestDifferentPlatform(unittest.TestCase):
    """test different platform."""

    def setUp(self):
        """set up func."""
        self.message = ''
        mock_profile.data = DEFAULT_PROFILE_DATA

    def test_default_mock(self, mock_sys, mock_subprocess):
        """test using default mock obj."""
        tts(self.message)
        # NOTE: the default for linux/win32 with gender male.
        # ( see non-exitent 'ven+f3' flag)
        mock_call = mock.call.call(['espeak', '-s170', self.message])
        assert mock_call in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_darwin_platform(self, mock_sys, mock_subprocess):
        """test darwin platform."""
        mock_sys.platform = 'darwin'
        tts(self.message)
        # NOTE: the default for macos with gender female.
        # (it don't have 'valex' flag)
        mock_call = mock.call.call(['say', self.message])
        assert mock_call in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_darwin_platform_female_gender(self, mock_sys, mock_subprocess):
        """test darwin platform."""
        mock_sys.platform = 'darwin'
        DEFAULT_PROFILE_DATA['va_gender'] = 'female'
        mock_profile.data = DEFAULT_PROFILE_DATA
        tts(self.message)
        # NOTE: the default for macos with gender female.
        # (it don't have 'valex' flag)
        mock_call = mock.call.call(['say', self.message])
        assert mock_call in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_darwin_platform_random_gender(self, mock_sys, mock_subprocess):
        """test darwin platform."""
        mock_sys.platform = 'darwin'
        gender = get_random_string(exclude_list=('female', 'male'))
        DEFAULT_PROFILE_DATA['va_gender'] = gender
        mock_profile.data = DEFAULT_PROFILE_DATA
        tts(self.message)
        # NOTE: the default for macos with gender female.
        # (it don't have 'valex' flag)
        mock_call = mock.call.call(['say', self.message])
        assert mock_call in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_darwin_platform_male_gender(self, mock_sys, mock_subprocess):
        """test darwin platform and male gender."""
        mock_sys.platform = 'darwin'
        DEFAULT_PROFILE_DATA['va_gender'] = 'male'
        mock_profile.data = DEFAULT_PROFILE_DATA
        tts(self.message)
        mock_call = mock.call.call(['say', '-valex', self.message])
        assert mock_call in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_random_platform(self, mock_sys, mock_subprocess):
        """test random platform."""
        mock_sys.platform = get_random_string(
            exclude_list=('linux', 'darwin', 'win32')
        )
        tts(self.message)
        # empty list/mock_subprocess not called
        assert not mock_subprocess.mock_calls

    def test_linux_win32_platform(self, mock_sys, mock_subprocess):
        """test linux and win32 platform."""
        for platform in ['linux', 'win32']:
            mock_sys.platform = platform
            tts(self.message)
            # NOTE: the default for linux/win32 with gender male.
            # ( see non-exitent 'ven+f3' flag)
            mock_call = mock.call.call(['espeak', '-s170', self.message])
            assert mock_call in mock_subprocess.mock_calls
            assert len(mock_subprocess.mock_calls) == 1

            # reset mock_subprocess
            mock_subprocess.reset_mock()

    def test_linux_win32_platf_female_gender(self, mock_sys, mock_subprocess):
        """test linux and win32 platform."""
        mock_profile.data = {'va_gender': 'female'}
        for platform in ['linux', 'win32']:
            mock_sys.platform = platform
            DEFAULT_PROFILE_DATA['tts'] = mock.Mock()
            mock_profile.data = DEFAULT_PROFILE_DATA
            tts(self.message)
            # NOTE: the default for linux/win32 with gender male.
            # ( see non-exitent 'ven+f3' flag)
            mock_call = mock.call.call(
                ['espeak', '-s170', self.message]
            )
            assert mock_call in mock_subprocess.mock_calls
            assert len(mock_subprocess.mock_calls) == 1

            # reset mock_subprocess
            mock_subprocess.reset_mock()

    def test_linux_win32_platf_random_gender(self, mock_sys, mock_subprocess):
        """test linux and win32 platform."""
        mock_profile.data = {
            'va_gender': get_random_string(exclude_list=('male', 'female')),
            'tts': mock.Mock(),
        }
        for platform in ['linux', 'win32']:
            mock_sys.platform = platform
            tts(self.message)
            # NOTE: the default for linux/win32 with gender male.
            # ( see non-exitent 'ven+f3' flag)
            mock_call = mock.call.call(['espeak', '-s170', self.message])
            assert mock_call in mock_subprocess.mock_calls
            assert len(mock_subprocess.mock_calls) == 1

            # reset mock_subprocess
            mock_subprocess.reset_mock()

    def test_linux_win32_platform_male_gender(self, mock_sys, mock_subprocess):
        """test linux and win32 platform."""
        mock_profile.data['va_gender'] = 'male'
        for platform in ('linux', 'win32'):
            mock_sys.platform = platform
            tts(self.message)
            mock_call = mock.call.call(['espeak', '-s170', self.message])
            assert mock_call in mock_subprocess.mock_calls
            assert len(mock_subprocess.mock_calls) == 1

            # reset mock_subprocess
            mock_subprocess.reset_mock()

    def test_pyvona(self, mock_sys, mock_subprocess):
        """test pyvona."""
        random_gender = get_random_string(
            exclude_list=('female', 'male')
        )
        mock_access_key = mock.Mock()
        mock_secret_key = mock.Mock()
        for gender in ('male', 'female', random_gender):
            mock_profile.data = {
                'va_gender': gender,
                'tts': 'ivona',
                'ivona': {
                    'access_key': mock_access_key,
                    'secret_key': mock_secret_key,
                }
            }
            with mock.patch('melissa.tts.pyvona') as mock_pyvona:
                tts(self.message)
                # test voice name
                assert len(mock_pyvona.mock_calls) == 2
                # test voice name
                if gender == 'female':
                    assert mock_pyvona.create_voice().voice_name == 'Salli'
                elif gender == 'male':
                    assert mock_pyvona.create_voice().voice_name == 'Joey'
                else:
                    assert mock_pyvona.create_voice().voice_name == 'Joey'
                create_voice_call = mock.call.create_voice(
                    mock_access_key, mock_secret_key
                )
                assert create_voice_call in mock_pyvona.mock_calls
                engine_speak_call = mock.call.create_voice().speak(
                    self.message
                )
                assert engine_speak_call in mock_pyvona.mock_calls
