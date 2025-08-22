class CommonMixin:
    
    def update(self, parts):
        self.parts = parts
        self.content = self.join_parts(self.parts)
        self.parsed = "\n\n".join(self.parts)
        self.count = len(self.parts)

    def join_parts(self, content):
        return f"\n{self.separator}\n".join(content)
