import re

with open('motor_popup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update all buttons
# Standard button class:
btn_class = 'w-full text-xs font-bold py-1 px-2 rounded border border-slate-600 bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors shadow-sm uppercase'

def replace_button_class(m):
    button_tag = m.group(0)
    # Don't make SVG button have standard class
    if 'svg' in button_tag:
        return button_tag
    if 'class="' in button_tag:
        return re.sub(r'class="[^"]*"', f'class="{btn_class}"', button_tag, count=1)
    else:
        return button_tag.replace('>', f' class="{btn_class}">')

text = re.sub(r'<button[^>]*>', replace_button_class, text)


# 2. Update panel headers
headers = ['Drive', 'Calibration', 'Dynamics', 'Backlash', 'Jog Control', 'Homing', 'Servo \(PID\)', 'STATUS', 'Resolution & Setup']
new_header_container_class = 'bg-slate-700/50 px-2 py-1 border-b border-slate-700 flex justify-between items-center group/header'
new_span_class = 'text-sm font-black text-slate-300 uppercase tracking-widest'

def replace_span_class(m):
    span_tag = m.group(0)
    content_match = re.search(r'>([^<]+)</span>', span_tag)
    if content_match:
        content = content_match.group(1).replace('\n', ' ').replace('\r', ' ').strip()
        content = ' '.join(content.split())
        for h in headers:
            h_clean = h.replace('\\', '')
            if h_clean == content:
                return re.sub(r'class="[^"]*"', f'class="{new_span_class}"', span_tag, count=1)
    return span_tag

# Regex to find spans
text = re.sub(r'<span\s+class="[^"]*"[^>]*>[^<]+</span>', replace_span_class, text)

# Now specifically the parent div of the panel headers
def fix_div_class(m):
    div_start = m.group(1) # `<div `
    div_end = m.group(2)   # `>`
    whitespace = m.group(3) # `\s*`
    span_full = m.group(4) # `<span class="...">Header</span>`
    
    return f'{div_start}class="{new_header_container_class}"{div_end}{whitespace}{span_full}'

pattern = r'(<div\s+)class="[^"]*"([^>]*>)(\s*)(<span\s+class="' + re.escape(new_span_class) + r'"[^>]*>[^<]+</span>)'
text = re.sub(pattern, fix_div_class, text)

with open('motor_popup.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("UI fixes applied successfully.")
