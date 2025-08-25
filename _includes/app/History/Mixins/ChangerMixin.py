from ...Utility import write_file

class ChangerMixin:

    def join_and_write(self):
        self.update(self.parts)
        write_file(self.path, self.content, self.config, "w")

    def append_history(self, content: str, update: bool = False) -> None:
        self.parts[-1] += content
        if update: self.update(self.parts)
        write_file(self.path, content, self.config)
        
    def append_separator(self) -> None:
        content = f"\n{self.separator}\n"

        self.parts.append("")
        self.update(self.parts)

        write_file(self.path, content, self.config)