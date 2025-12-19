from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import re

class HorizontalRulePreprocessor(Preprocessor):
    """Convert different dash counts to different hr weights."""

    def run(self, lines):
        new_lines = []
        for line in lines:
            # Check if line is only dashes (and optional whitespace)
            stripped = line.strip()
            if re.match(r'^-+$', stripped):
                dash_count = len(stripped)
                if dash_count == 3:
                    # Standard hr
                    new_lines.append('<hr class="hr-heavy">')
                elif dash_count == 4:
                    # Medium hr
                    new_lines.append('<hr class="hr-medium">')
                elif dash_count == 5:
                    # Light hr
                    new_lines.append('<hr class="hr-light">')
                elif dash_count >= 6:
                    # Mini hr (30% width, left-aligned)
                    new_lines.append('<hr class="hr-mini">')
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines

class HorizontalRuleExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(HorizontalRulePreprocessor(md), 'hr_weights', 100)

def makeExtension(**kwargs):
    return HorizontalRuleExtension(**kwargs)
