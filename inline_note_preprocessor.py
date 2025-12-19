"""
Custom Markdown preprocessor for inline notes on code blocks.

Syntax:
```language
code here
```
!!! note inline
    This note appears on the same line as the code block
"""

import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension


class InlineNotePreprocessor(Preprocessor):
    """Preprocessor to handle inline notes next to code blocks."""

    def run(self, lines):
        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check if this is the start of a fenced code block
            if re.match(r'^```', line):
                # Collect the entire code block
                code_block = [line]
                i += 1

                # Find the end of the code block
                while i < len(lines) and not re.match(r'^```\s*$', lines[i]):
                    code_block.append(lines[i])
                    i += 1

                # Add the closing ```
                if i < len(lines):
                    code_block.append(lines[i])
                    i += 1

                # Check if the next non-empty line is an inline admonition
                if i < len(lines):
                    # Skip empty lines but remember them
                    skipped_lines = []
                    temp_i = i
                    while temp_i < len(lines) and lines[temp_i].strip() == '':
                        skipped_lines.append(lines[temp_i])
                        temp_i += 1

                    # Check if we found an admonition with "inline" marker
                    if temp_i < len(lines):
                        admon_match = re.match(r'^!!!\s+(\w+)\s+inline\s*$', lines[temp_i])
                        if admon_match:
                            # Found an inline admonition!
                            admon_type = admon_match.group(1)
                            i = temp_i + 1

                            # Collect the admonition content (indented lines)
                            admon_content = []
                            while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                                if lines[i].strip():  # Skip empty lines in admonition
                                    admon_content.append(lines[i][4:])  # Remove 4-space indent
                                i += 1

                            # Create the wrapper HTML with markdown="1" to allow markdown processing
                            new_lines.append('<div class="code-with-inline-note" markdown="1">')
                            new_lines.append('<div class="inline-code-block" markdown="1">')
                            new_lines.extend(code_block)
                            new_lines.append('</div>')
                            new_lines.append(f'<div class="inline-note inline-note-{admon_type}" markdown="1">')
                            new_lines.append(f'<div class="inline-note-title">{admon_type.title()}</div>')
                            new_lines.append('')  # Empty line to ensure markdown processing
                            new_lines.extend(admon_content)
                            new_lines.append('')  # Empty line to ensure markdown processing
                            new_lines.append('</div>')
                            new_lines.append('</div>')
                            continue
                        else:
                            # Not an inline admonition, add code block and skipped lines normally
                            new_lines.extend(code_block)
                            new_lines.extend(skipped_lines)
                            i = temp_i
                            continue

                # No inline note found, just add the code block
                new_lines.extend(code_block)
            else:
                new_lines.append(line)
                i += 1

        return new_lines


class InlineNoteExtension(Extension):
    """Extension to enable inline notes on code blocks."""

    def extendMarkdown(self, md):
        md.preprocessors.register(InlineNotePreprocessor(md), 'inline_note', 27)


def makeExtension(**kwargs):
    return InlineNoteExtension(**kwargs)
