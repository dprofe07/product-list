import re


class ListItem:
    def __init__(self, text, checked=False):
        self.text = text
        self.checked = checked

    def __repr__(self):
        return f"ListItem({self.text}, {self.checked})"

    @property
    def is_label(self):
        return self.text.startswith('~')

    def ifck(self, txt):
        if self.is_label:
            return ''
        return txt if self.checked else ''

    def to_export_view(self):
        if self.is_label:
            return '----- ' + self.text[1:] + ' -----'
        return re.sub(r'#\((\d+)\)', '\\1', self.text)

    def to_editing_view(self):
        return self.ifck('!') + self.text

    def to_default_view(self, idx):
        if self.is_label:
            return f'<p> ----- {self.text[1:]} -----</p>'
        c = -1
        def proceed(m):
            nonlocal c
            c += 1
            return f'<input type="number" min="0" max="15" step="1" value="{m.group(1)}" id="spn_{idx}_{c}"/>'
        prep_text = re.sub(r'#\((\d+)\)', proceed, self.text)

        return f'''<p><label><input type="checkbox" id="chk_{idx}" {self.ifck('checked')}/>{prep_text}</label></p>'''