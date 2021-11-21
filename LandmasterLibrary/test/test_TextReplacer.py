from TextReplacer import ReplaceCharacter

class Test_ReplaceCharacter:
    def test_MakeVoicedsound_1(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('がぎぐげござじずぜぞ') == 'がぎぐげござじずぜぞ'

    def test_MakeVoicedsound_2(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('だぢづでどばびぶべぼ') == 'だぢづてどばびぶべぼ'

    def test_MakeVoicedsound_3(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ぱぴぷぺぽ') == 'ぱぴぷぺぽ'

    def test_MakeVoicedsound_4(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('がぎぐげござじずぜぞ') == 'がぎぐげござじずぜぞ'

    def test_MakeVoicedsound_5(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('だぢづてどばびぶべぼ') == 'だぢづてどばびぶべぼ'

    def test_MakeVoicedsound_6(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ぱぴぷぺぽ') == 'ぱぴぷぺぽ'

