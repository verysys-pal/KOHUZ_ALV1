import re
from bs4 import BeautifulSoup

with open('motor_popup.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

button_class = "text-xs font-bold py-1 px-2 rounded border border-slate-600 bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors uppercase w-full shadow-sm"

# 1. Update all buttons
for btn in soup.find_all('button'):
    # Keep some id or layout if needed? The instruction says: 
    # "모든 버튼의 크기와 폰트 크기, 색상, 배경등 속성을 동일하게 수정"
    btn['class'] = button_class

# 2. Update panel headers
# Drive, Calibration, Dynamics, Backlash, Jog Control, Homing, Servo (PID), STATUS, Resolution & Setup
headers = ['Drive', 'Calibration', 'Dynamics', 'Backlash', 'Jog Control', 'Homing', 'Servo (PID)', 'STATUS', 'Resolution & Setup']
header_texts = soup.find_all('span')

for span in header_texts:
    text = span.get_text().strip()
    if text.upper() in [h.upper() for h in headers]:
        # Update span
        span['class'] = "text-sm font-black text-slate-300 uppercase tracking-widest"
        # Update parent div
        parent = span.parent
        # The parent is the header div
        if parent.name == 'div':
            parent['class'] = "bg-slate-700/50 px-2 py-1 border-b border-slate-700 flex justify-between items-center group/header"

with open('motor_popup.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("done")
