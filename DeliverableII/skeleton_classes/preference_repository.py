from .preference import Preference

class PreferenceRepository:
    def getPreference(self, userId: str) -> Preference:
        pass

    def savePreference(self, pref: Preference):
        pass
