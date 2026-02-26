import re
with open("dashboard.html", "r") as f:
    html = f.read()

# Replace the alert logic with a confirm dialog
old_logic = """            const dmovEl = document.querySelector(`[data-led-pv="${pvPrefix}.DMOV"]`);
            if (dmovEl && !dmovEl.classList.contains('on')) {
                alert(`Cannot change parameters while Motor ${axisIndex + 1} is moving (DMOV != 1).`);
                event.target.value = '';
                return;
            }"""

new_logic = """            const dmovEl = document.querySelector(`[data-led-pv="${pvPrefix}.DMOV"]`);
            if (dmovEl && !dmovEl.classList.contains('on')) {
                const proceed = confirm(`Motor ${axisIndex + 1} appears to be moving or is disconnected (DMOV != 1).\\nAre you sure you want to apply parameters?`);
                if (!proceed) {
                    event.target.value = '';
                    return;
                }
            }"""

html = html.replace(old_logic, new_logic)
with open("dashboard.html", "w") as f:
    f.write(html)
