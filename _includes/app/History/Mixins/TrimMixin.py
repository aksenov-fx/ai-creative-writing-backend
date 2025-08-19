class TrimMixin:
    
    def estimate_tokens(self) -> int:
        return len(self.content) // self.config.TOKEN_ESTIMATION_DIVISOR
        
    def trim_content(self) -> str:
        current_tokens = self.estimate_tokens()
        
        while current_tokens > self.config.max_tokens and self.count >= self.parts_to_trim:
            self.parts = self.parts[self.parts_to_trim:]
            self.update(self.parts)
            self.removed_parts += self.parts_to_trim
            current_tokens = self.estimate_tokens()

        if self.removed_parts: print(f"\nRemoved {self.removed_parts} text parts to fit the token limit.")
        return self
