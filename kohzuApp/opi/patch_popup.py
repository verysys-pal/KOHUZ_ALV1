import re

with open('/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/opi/motor_popup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace all text-[8px], text-[9px], text-[10px], text-[11px], text-[12px] with text-xs
text = re.sub(r'text-\[(8|9|10|11|12)px\]', 'text-xs', text)

# 헤더 메인: text-sm -> text-lg
text = text.replace('class="text-sm font-bold text-white truncate block">Axis 1', 'class="text-lg font-bold text-white truncate block">Axis 1')

# 패널 헤더/섹션 명: text-xs -> text-sm
text = text.replace('class="text-xs font-black text-blue-400 uppercase tracking-widest">Drive', 'class="text-sm font-black text-blue-400 uppercase tracking-widest">Drive')
text = text.replace('class="text-xs font-black text-indigo-400 uppercase tracking-widest">Calibration', 'class="text-sm font-black text-indigo-400 uppercase tracking-widest">Calibration')
text = text.replace('class="text-xs font-black text-blue-400 uppercase tracking-widest">Dynamics', 'class="text-sm font-black text-blue-400 uppercase tracking-widest">Dynamics')
text = text.replace('class="text-xs font-black text-slate-300 uppercase">Backlash', 'class="text-sm font-black text-slate-300 uppercase">Backlash')
text = text.replace('class="text-xs font-black text-slate-300 uppercase">Jog Control', 'class="text-sm font-black text-slate-300 uppercase">Jog Control')
text = text.replace('class="text-xs font-black text-slate-300 uppercase">Servo (PID)', 'class="text-sm font-black text-slate-300 uppercase">Servo (PID)')
text = re.sub(r'class="text-xs font-black text-slate-300 uppercase tracking-widest">Resolution\s*&\s*Setup', 'class="text-sm font-black text-slate-300 uppercase tracking-widest">Resolution & Setup', text)
text = text.replace('class="text-xs font-black text-slate-200 uppercase tracking-widest">STATUS', 'class="text-sm font-black text-slate-200 uppercase tracking-widest">STATUS')

# "Mechanical Specifications" and "Driver & Switching Settings" headers use text-xs currently, move to text-sm
text = text.replace('class="text-xs font-black text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-2">', 'class="text-sm font-black text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-2">')

# Move 메인 입력란: it became text-xs after first regex. Change to text-sm.
text = text.replace('class="bg-blue-900/10 border border-blue-500/30 rounded px-1 py-0.5 text-xs text-right text-white font-bold outline-none', 'class="bg-blue-900/10 border border-blue-500/30 rounded px-1 py-0.5 text-sm text-right text-white font-bold outline-none')

# 본문 안내문 "Note: ..." -> text-sm
text = text.replace('class="text-xs text-slate-500 italic leading-relaxed">', 'class="text-sm text-slate-500 italic leading-relaxed">')

with open('/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/opi/motor_popup.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied replacements!")
