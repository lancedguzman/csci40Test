from Match import Match


class Regex():
    """This python file implements a basic Regex pattern matching algorithm.

    Classes: Contains methods for regex search, match, findall, parse_span,
    parse_range, and check_char.

    Author : Lorenzo Duenas
    """

    @staticmethod
    def search(pattern, string):
        """Searches through a pattern of strings.

        Scan through the given string looking for the first location
        where the regular expression produces a match
        """
        if not isinstance(pattern, str) or not isinstance(string, str):
            return None

        # Initialize containers / values.
        input_char_pointer = [0]
        meta_char_pointer = [0]

        span_start = 0
        span_end = 0

        loop_end = True

        pattern_length = len(pattern)
        input_length = len(string)

        previous_bool = False
        match_found = False

        while loop_end:

            # Check if the whole string was searched.
            if (meta_char_pointer[0] == (pattern_length) or
                input_char_pointer[0] == (input_length)) and \
                    match_found is False:
                return None

            # Check character one by one. Pointers are incremented here.
            result = Regex.check_char(
                string, pattern,
                input_char_pointer, meta_char_pointer)

            if result is False:

                # Reset pattern pointers.
                if previous_bool is True:
                    previous_bool = False
                    meta_char_pointer[0] = 0
                    input_char_pointer[0] -= 1

                input_char_pointer[0] += 1
                continue

            # Save span_start.
            if previous_bool is False:
                previous_bool = True
                span_start = input_char_pointer[0] - 1

            # The whole pattern was successfully matched.
            if meta_char_pointer[0] == (pattern_length):
                break

        # Compute for value of span.
        span_end = input_char_pointer[0]
        span = "(" + str(span_start) + ", " + str(span_end) + ")"

        # Create and return Match object.
        match_object = Match(span, string[span_start:span_end])
        return match_object

    @staticmethod
    def match(pattern, string):
        """Matches corresponding characters.

        Returns a corresponding match() object if zero or more
        characters at the beginning of string match the pattern,
        else returns a None
        """
        if not isinstance(pattern, str) or not isinstance(string, str):
            return None

        # Initialize containers/ values.
        input_char_pointer = [0]
        meta_char_pointer = [0]

        span_start = 0
        span_end = 0

        loop_end = True

        pattern_length = len(pattern)
        input_length = len(string)

        while loop_end:

            # Check character one by one. Pointers are incremented here.
            result = Regex.check_char(
                string, pattern,
                input_char_pointer, meta_char_pointer)

            # Check if first character is not a match.
            if input_char_pointer[0] == 0 and result is False:
                return None

            # Check if succeeding characters aren't a match.
            if result is False:
                return None

            # Check if all characters in pattern have been processed.
            if meta_char_pointer[0] == (pattern_length) or \
                    input_char_pointer[0] == (input_length):
                break

        # Compute for value of span.
        span_end = input_char_pointer[0]
        span = "(" + str(span_start) + ", " + str(span_end) + ")"

        # Create and return Match object.
        match_object = Match(span, string[span_start:span_end])
        return match_object

    @staticmethod
    def findall(pattern, string):
        """Finds all the possible matches.

        Finds all possible matches in the entire string and
        returns them as a list of strings
        """
        match_list = []
        span_set = set()
        string_len = len(string)

        # Evaluate a shrinking string.
        for x in range(0, string_len):
            match_object = Regex.search(pattern, string[x:])

            if match_object is None:
                continue

            # Parse the span objects to remove duplicates
            temp_span = Regex.parse_span(match_object.span, x)

            # Check for possible duplicates
            if temp_span not in span_set:
                match_list.append(match_object.match)
                span_set.add(temp_span)

        return match_list

    @staticmethod
    def parse_span(string_input, offset):
        """Parses a string input.

        Gets a span string, and increases it based on an offset.
        """
        # Convert span into integers
        span_list = string_input.split(", ")
        span_start = int(span_list[0].strip("()"))
        span_end = int(span_list[1].strip("()"))

        span_start += offset
        span_end += offset

        return "(" + str(span_start) + ", " + str(span_end) + ")"

    @staticmethod
    def parse_range(char_input, meta_range):
        """Parses the range of characters.

        Determines if a character falls under a specified range.
        """
        char_set = set()

        # No "-"; only check characters in string.
        if meta_range.find("-") == -1:
            if char_input not in meta_range:
                return False

        try:
            # Get left, and right, then get all other ascii in-between.
            char_left = meta_range[meta_range.find("-") - 1]
            char_right = meta_range[meta_range.find("-") + 1]
            for x in range(ord(char_left), ord(char_right) + 1):
                char_set.add(chr(x))
        except IndexError:
            print("unknown error")
            return False

        if char_input not in char_set:
            return False

        return True

    @staticmethod
    def check_char(
        char_input, meta_character, input_pointer,
        meta_pointer):
        """Checks the characters if it is a match.

        Checks if a character matches a specific
        meta character archetype.
        """
        # No newline characters.
        if meta_character[meta_pointer[0]] == ".":
            if char_input[input_pointer[0]] == "\n":
                return False

        # Check if the backslash has another input.
        elif meta_character[meta_pointer[0]] == "\\":
            meta_pointer[0] += 1

            # Alphanumeric only
            if meta_character[meta_pointer[0]] == "w":
                if not char_input[input_pointer[0]].isalnum():
                    return False

            # Non-Alphanumeric only
            elif meta_character[meta_pointer[0]] == "W":
                if char_input[input_pointer[0]].isalnum():
                    return False

        # Get range inside brackets.
        elif meta_character[meta_pointer[0]] == "[":
            meta_pointer[0] += 1
            char_range = ""
            while meta_character[meta_pointer[0]] != "]":
                char_range += str(meta_character[meta_pointer[0]])
                meta_pointer[0] += 1
            if not Regex.parse_range(char_input[input_pointer[0]], char_range):
                return False

        # Check for repeating characters.
        elif meta_character[meta_pointer[0]] == "+":
            try:
                last_char = meta_character[meta_pointer[0] - 1]
                while char_input[input_pointer[0]] == last_char:
                    input_pointer[0] += 1
            except IndexError:
                print("idx_e")
                return False
            finally:
                input_pointer[0] -= 1

        # Check if specified, normal character.
        else:
            if meta_character[meta_pointer[0]] != char_input[input_pointer[0]]:
                return False

        input_pointer[0] += 1
        meta_pointer[0] += 1

        return True
