class ParserMixin:
    """Common parsing methods for History and Summary parsers."""
    
    def cut_history_to_part_number(self, part_number):
        self.update(self.parts[:part_number])
        return self

    def set_part_number_content(self, part_number):
        self.part_number_content = self.parts[part_number-1]
        return self

    def set_to_previous_part(self):
        self.update(self.parts[-2:-1])
        return self

    def cut(self, part_number, include_previous_part):
        if not include_previous_part: 
            self.content = ""
            self.parts = []
            self.parsed = ""
            return self

        self.cut_history_to_part_number(part_number)
        self.set_part_number_content(part_number)
        self.set_to_previous_part()
        return self
