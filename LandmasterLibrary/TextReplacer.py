class ReplaceCharacter:
    def MakeVoicedsound(self, text):
        """
        text           : String of target text.
        """
        target  = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
        replace = 'がぎぐげござじずぜぞだぢづてどばびぶべぼぱぴぷぺぽガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
        list_target  = []
        list_replace = []
        for i in range(0, len(target), 2):
            list_target.append(target[i : i+2])
        for i in range(0, len(replace), 1):
            list_replace.append(replace[i : i+1])

        for i in range(0,len(list_target)):
            text = text.replace(list_target[i], list_replace[i])

        return text
