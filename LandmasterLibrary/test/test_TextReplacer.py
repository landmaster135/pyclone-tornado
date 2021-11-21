from TextReplacer import ReplaceCharacter

class Test_ReplaceCharacter:
    # Unicode : \u3099
    def test_MakeVoicedsound_1_1(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('がぎぐげござじずぜぞ') == 'がぎぐげござじずぜぞ'

    def test_MakeVoicedsound_1_2(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('だぢづでどばびぶべぼ') == 'だぢづてどばびぶべぼ'

    # Unicode : \u309A
    def test_MakeVoicedsound_1_3(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ぱぴぷぺぽ') == 'ぱぴぷぺぽ'

    # Unicode : \u3099
    def test_MakeVoicedsound_1_4(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ガギグゲゴザジズゼゾ') == 'ガギグゲゴザジズゼゾ'

    def test_MakeVoicedsound_1_5(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ダヂヅデドバビブベボ') == 'ダヂヅデドバビブベボ'

    # Unicode : \u309A
    def test_MakeVoicedsound_1_6(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('パピプペポ') == 'パピプペポ'

    # dakuon
    def test_MakeVoicedsound_2_1(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('がぎぐげござじずぜぞ') == 'がぎぐげござじずぜぞ'

    def test_MakeVoicedsound_2_2(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('だぢづてどばびぶべぼ') == 'だぢづてどばびぶべぼ'

    #handakuon
    def test_MakeVoicedsound_2_3(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ぱぴぷぺぽ') == 'ぱぴぷぺぽ'

    # dakuon
    def test_MakeVoicedsound_2_4(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ガギグゲゴザジズゼゾ') == 'ガギグゲゴザジズゼゾ'

    def test_MakeVoicedsound_2_5(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('ダヂヅデドバビブベボ') == 'ダヂヅデドバビブベボ'

    # handakuon
    def test_MakeVoicedsound_2_6(self):
        replaceCharacter = ReplaceCharacter()
        assert replaceCharacter.MakeVoicedsound('パピプペポ') == 'パピプペポ'

