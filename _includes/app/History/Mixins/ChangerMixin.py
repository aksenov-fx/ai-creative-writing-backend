class ChangerMixin:

    def join_and_write(self):
        from ...Utility import write_file
        self.update(self.parts)
        write_file(self.path, self.content)

    def append_history(self, content: str, update: bool = False) -> None:
        self.parts[-1] += content
        if update: self.update(self.parts)
        with open(self.path, 'a', encoding='utf-8') as f: f.write(content)
        