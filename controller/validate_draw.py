class ValidateDraw:
    def validate_entry(self, num):
        if num == '':
            return True
        try:
            value = int(num)
        except ValueError:
            return False
        return 1 <= value <= 100

    def validate_command(self):
        self.vcmd = (self.root.register(self.validate_entry), '%P')
