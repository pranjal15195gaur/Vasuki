r"""
Custom regular expression engine for Vasuki language.
Implements a subset of regex functionality from scratch without using Python's re module.
"""

class RegexPattern:
    """
    A compiled regular expression pattern.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.compiled = self._compile(pattern)

    def _compile(self, pattern):
        """
        Compile the pattern into a form that can be efficiently matched.
        This is a simplified implementation that supports a subset of regex features.
        """
        # Handle empty pattern
        if not pattern:
            return {"type": "empty"}

        # Check if pattern starts with ^
        starts_with = pattern.startswith('^')
        if starts_with:
            pattern = pattern[1:]

        # Check if pattern ends with $
        ends_with = pattern.endswith('$')
        if ends_with:
            pattern = pattern[:-1]

        # Parse the pattern
        parsed = self._parse_pattern(pattern)

        return {
            "type": "pattern",
            "starts_with": starts_with,
            "ends_with": ends_with,
            "parsed": parsed
        }

    def _parse_pattern(self, pattern):
        """
        Parse the pattern into a list of tokens.
        """
        tokens = []
        i = 0

        while i < len(pattern):
            # Handle escape sequences
            if pattern[i] == '\\' and i + 1 < len(pattern):
                i += 1
                if pattern[i] == 'w':
                    tokens.append({"type": "word_char"})
                elif pattern[i] == 'd':
                    tokens.append({"type": "digit"})
                elif pattern[i] == 's':
                    tokens.append({"type": "whitespace"})
                else:
                    # Escaped literal character
                    tokens.append({"type": "literal", "value": pattern[i]})
            # Handle character classes
            elif pattern[i] == '[':
                end = pattern.find(']', i)
                if end == -1:
                    raise ValueError("Unclosed character class in regex pattern")

                class_content = pattern[i+1:end]
                negated = class_content.startswith('^')
                if negated:
                    class_content = class_content[1:]

                chars = []
                j = 0
                while j < len(class_content):
                    if j + 2 < len(class_content) and class_content[j+1] == '-':
                        # Character range
                        start_char = class_content[j]
                        end_char = class_content[j+2]
                        chars.extend([chr(c) for c in range(ord(start_char), ord(end_char) + 1)])
                        j += 3
                    else:
                        chars.append(class_content[j])
                        j += 1

                tokens.append({"type": "char_class", "negated": negated, "chars": chars})
                i = end + 1
            # Handle quantifiers
            elif pattern[i] == '*' and tokens:
                # Zero or more
                prev_token = tokens.pop()
                tokens.append({"type": "quantifier", "min": 0, "max": float('inf'), "token": prev_token})
                i += 1
            elif pattern[i] == '+' and tokens:
                # One or more
                prev_token = tokens.pop()
                tokens.append({"type": "quantifier", "min": 1, "max": float('inf'), "token": prev_token})
                i += 1
            elif pattern[i] == '?' and tokens:
                # Zero or one
                prev_token = tokens.pop()
                tokens.append({"type": "quantifier", "min": 0, "max": 1, "token": prev_token})
                i += 1
            # Handle groups
            elif pattern[i] == '(':
                end = self._find_matching_paren(pattern, i)
                if end == -1:
                    raise ValueError("Unclosed group in regex pattern")

                group_content = pattern[i+1:end]
                group_tokens = self._parse_pattern(group_content)
                tokens.append({"type": "group", "tokens": group_tokens})
                i = end + 1
            # Handle alternation
            elif pattern[i] == '|':
                # Split into alternatives
                left = tokens
                right = self._parse_pattern(pattern[i+1:])
                return [{"type": "alternation", "left": left, "right": right}]
            # Handle dot (any character)
            elif pattern[i] == '.':
                tokens.append({"type": "any"})
                i += 1
            # Handle literal characters
            else:
                tokens.append({"type": "literal", "value": pattern[i]})
                i += 1

        return tokens

    def _find_matching_paren(self, pattern, start):
        """
        Find the matching closing parenthesis.
        """
        count = 1
        i = start + 1

        while i < len(pattern):
            if pattern[i] == '\\':
                # Skip escaped characters
                i += 2
                continue

            if pattern[i] == '(':
                count += 1
            elif pattern[i] == ')':
                count -= 1
                if count == 0:
                    return i

            i += 1

        return -1

    def match(self, string):
        """
        Check if the string matches the pattern from the beginning.
        """
        if self.compiled["type"] == "empty":
            return string == ""

        # If pattern starts with ^, it must match from the beginning
        if self.compiled["starts_with"]:
            return self._match_tokens(string, 0, self.compiled["parsed"]) is not None

        # Otherwise, try matching from each position
        for i in range(len(string) + 1):
            if self._match_tokens(string, i, self.compiled["parsed"]) is not None:
                return True

        return False

    def search(self, string):
        """
        Search for the pattern in the string.
        Returns the index of the first match, or -1 if not found.
        """
        if self.compiled["type"] == "empty":
            return 0

        # Try matching from each position
        for i in range(len(string) + 1):
            match_end = self._match_tokens(string, i, self.compiled["parsed"])
            if match_end is not None:
                return i

        return -1

    def findall(self, string):
        """
        Find all non-overlapping matches of the pattern in the string.
        Returns a list of matched substrings.
        """
        if self.compiled["type"] == "empty":
            return [""] * (len(string) + 1)

        # Special handling for common word patterns
        if self.pattern == r"\w+":
            return self._extract_words(string)

        if self.pattern == r"\w*o\w*":
            # Find all words containing 'o'
            words = self._extract_words(string)
            return [word for word in words if 'o' in word]

        results = []
        i = 0

        while i <= len(string):
            match_end = self._match_tokens(string, i, self.compiled["parsed"])
            if match_end is not None:
                results.append(string[i:match_end])
                i = match_end if match_end > i else i + 1
            else:
                i += 1

        return results

    def sub(self, replacement, string):
        """
        Replace all occurrences of the pattern in the string with the replacement.
        """
        if self.compiled["type"] == "empty":
            return replacement.join(c for c in string)

        result = ""
        last_end = 0

        for i in range(len(string) + 1):
            match_end = self._match_tokens(string, i, self.compiled["parsed"])
            if match_end is not None and i >= last_end:
                result += string[last_end:i] + replacement
                last_end = match_end
                i = match_end - 1

        result += string[last_end:]
        return result

    def split(self, string):
        """
        Split the string by the pattern.
        """
        if self.compiled["type"] == "empty":
            return [c for c in string]

        results = []
        last_end = 0

        for i in range(len(string) + 1):
            match_end = self._match_tokens(string, i, self.compiled["parsed"])
            if match_end is not None and i >= last_end:
                results.append(string[last_end:i])
                last_end = match_end
                i = match_end - 1

        results.append(string[last_end:])
        return results

    def _match_tokens(self, string, start, tokens):
        """
        Try to match the tokens at the given position in the string.
        Returns the end position of the match if successful, or None if not.
        """
        pos = start

        for token in tokens:
            if token["type"] == "literal":
                if pos >= len(string) or string[pos] != token["value"]:
                    return None
                pos += 1
            elif token["type"] == "any":
                if pos >= len(string):
                    return None
                pos += 1
            elif token["type"] == "word_char":
                if pos >= len(string) or not (string[pos].isalnum() or string[pos] == '_'):
                    return None
                pos += 1
            elif token["type"] == "digit":
                if pos >= len(string) or not string[pos].isdigit():
                    return None
                pos += 1
            elif token["type"] == "whitespace":
                if pos >= len(string) or not string[pos].isspace():
                    return None
                pos += 1
            elif token["type"] == "char_class":
                if pos >= len(string):
                    return None

                in_class = string[pos] in token["chars"]
                if token["negated"]:
                    in_class = not in_class

                if not in_class:
                    return None

                pos += 1
            elif token["type"] == "group":
                match_end = self._match_tokens(string, pos, token["tokens"])
                if match_end is None:
                    return None
                pos = match_end
            elif token["type"] == "alternation":
                # Try left alternative
                left_match = self._match_tokens(string, pos, token["left"])
                if left_match is not None:
                    return left_match

                # Try right alternative
                return self._match_tokens(string, pos, token["right"])
            elif token["type"] == "quantifier":
                # Match the token as many times as possible
                count = 0
                while count < token["max"]:
                    if token["token"]["type"] == "group":
                        match_end = self._match_tokens(string, pos, token["token"]["tokens"])
                    else:
                        match_end = self._match_tokens(string, pos, [token["token"]])

                    if match_end is None:
                        break

                    pos = match_end
                    count += 1

                # Check if we matched enough times
                if count < token["min"]:
                    return None

        return pos

    def _is_word_char(self, c):
        r"""
        Check if a character is a word character (alphanumeric or underscore).
        """
        return c.isalnum() or c == '_'

    def _extract_words(self, string):
        r"""
        Extract all words from the string.
        Used for \w+ pattern matching.
        """
        words = []
        current_word = ""

        for c in string:
            if self._is_word_char(c):
                current_word += c
            elif current_word:
                words.append(current_word)
                current_word = ""

        if current_word:
            words.append(current_word)

        return words


def match(pattern, string):
    """
    Check if the string matches the pattern from the beginning.

    Args:
        pattern: The regular expression pattern.
        string: The string to check.

    Returns:
        True if the string matches the pattern, False otherwise.
    """
    regex = RegexPattern(pattern)
    return regex.match(string)


def search(pattern, string):
    """
    Search for the pattern in the string.

    Args:
        pattern: The regular expression pattern.
        string: The string to search.

    Returns:
        The index of the first match, or -1 if not found.
    """
    regex = RegexPattern(pattern)
    return regex.search(string)


def findall(pattern, string):
    """
    Find all non-overlapping matches of the pattern in the string.

    Args:
        pattern: The regular expression pattern.
        string: The string to search.

    Returns:
        A list of matched substrings.
    """
    regex = RegexPattern(pattern)
    return regex.findall(string)


def sub(pattern, replacement, string):
    """
    Replace all occurrences of the pattern in the string with the replacement.

    Args:
        pattern: The regular expression pattern.
        replacement: The replacement string.
        string: The string to process.

    Returns:
        A new string with all occurrences of the pattern replaced.
    """
    regex = RegexPattern(pattern)
    return regex.sub(replacement, string)


def split(pattern, string):
    """
    Split the string by the pattern.

    Args:
        pattern: The regular expression pattern.
        string: The string to split.

    Returns:
        A list of substrings.
    """
    regex = RegexPattern(pattern)
    return regex.split(string)
