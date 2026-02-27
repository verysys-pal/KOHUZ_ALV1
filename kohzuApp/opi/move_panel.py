import re

with open('motor_popup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the block
start_str = "                        <!-- Resolution & Setup Tools -->"
end_str = "                        </div>\n                    </div>\n\n                    <!-- Column 2: Status Panel -->"

start_idx = text.find(start_str)
end_idx = text.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find the block to extract")
    exit(1)

# The block to move
block = text[start_idx:end_idx]

# Remove the block from Column 1
text = text[:start_idx] + text[end_idx:]

# Find where to insert it in Column 2
# Column 2 looks like:
#                     <!-- Column 2: Status Panel -->
#                     <div class="space-y-4">
#                         <div class="border border-slate-700 rounded overflow-hidden sticky top-0">
# ...
#                         </div>    <-- this is what we need to find, it's followed by "                    </div>\n                </div>"

# Let's find the closing of the sticky div:
insert_search = """                                <!-- Utility Buttons -->
                                <div class="grid grid-cols-2 gap-2 mt-4">
                                    <button onclick="app.writePrefix('.SYNC', 1)"
                                        class="bg-indigo-900/20 hover:bg-indigo-900/40 border border-indigo-700/50 text-indigo-300 py-2 rounded text-xs font-black uppercase tracking-wider transition-all">Scan
                                        Params</button>
                                    <button onclick="app.writePrefix('.LOAD', 1)"
                                        class="bg-slate-700/40 hover:bg-slate-700/60 border border-slate-600 text-slate-300 py-2 rounded text-xs font-black uppercase tracking-wider transition-all">Load
                                        Settings</button>
                                </div>
                            </div>
                        </div>"""

insert_idx = text.find(insert_search)
if insert_idx == -1:
    print("Could not find insert location")
    exit(1)

insert_pos = insert_idx + len(insert_search) + 1 # +1 for newline

# Insert the block
# We can add a newline before the block to keep formatting nice
new_text = text[:insert_pos] + "\n" + block + text[insert_pos:]

with open('motor_popup.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Panel moved successfully")
