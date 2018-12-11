class MockedHP:
    def __init__(*args, **kwargs):
        pass

    def change(*args, **kwargs):
        pass

    def stat_value(*args, **kwargs):
        pass

    def __str__(*args, **kwargs):
        return 'Mocked HP'


class MockedStamina:
    value = 100

    def __init__(*args, **kwargs):
        pass

    def change(*args, **kwargs):
        pass

    @property
    def stat_value(self, *args, **kwargs):
        return self.value

    def __str__(*args, **kwargs):
        return 'Mocked Stamina'


class MockedMana:
    def __init__(*args, **kwargs):
        pass

    def change(*args, **kwargs):
        pass

    def stat_value(*args, **kwargs):
        pass

    def __str__(*args, **kwargs):
        return 'Mocked Stamina'


