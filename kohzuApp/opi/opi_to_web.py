import xml.etree.ElementTree as ET
import os

def parse_color(color_element):
    if color_element is None:
        return "black"
    color_node = color_element.find("color")
    if color_node is not None:
        r = color_node.get("red")
        g = color_node.get("green")
        b = color_node.get("blue")
        return f"rgb({r},{g},{b})"
    return "black"

def parse_font(font_element):
    if font_element is None:
        return "sans-serif"
    font_node = font_element.find("opifont.name")
    if font_node is not None:
        return font_node.get("fontName", "sans-serif")
    return "sans-serif"

def convert_widget(widget, parent_x=0, parent_y=0):
    w_type = widget.find("widget_type").text
    x = int(widget.find("x").text) + parent_x
    y = int(widget.find("y").text) + parent_y
    width = int(widget.find("width").text)
    height = int(widget.find("height").text)
    
    bg_color = parse_color(widget.find("background_color"))
    fg_color = parse_color(widget.find("foreground_color"))
    
    style = f"position: absolute; left: {x}px; top: {y}px; width: {width}px; height: {height}px; background-color: {bg_color}; color: {fg_color}; box-sizing: border-box;"
    
    pv_name = widget.find("pv_name").text if widget.find("pv_name") is not None else ""
    text = widget.find("text").text if widget.find("text") is not None else ""
    tooltip = widget.find("tooltip").text if widget.find("tooltip") is not None else ""

    html = ""
    
    if w_type == "Label":
        style += " display: flex; align-items: center; justify-content: center; overflow: hidden;"
        # Check alignment
        align = widget.find("horizontal_alignment")
        if align is not None:
            if align.text == "0": style += " justify-content: flex-start;"
            elif align.text == "1": style += " justify-content: center;"
            elif align.text == "2": style += " justify-content: flex-end;"
        html = f'<div style="{style}" title="{tooltip}">{text}</div>'
        
    elif w_type == "Text Update":
        style += " border: 1px solid #ccc; padding: 2px; font-family: monospace; overflow: hidden;"
        html = f'<div style="{style}" class="pv-readback" data-pv="{pv_name}" title="{tooltip}">{text if text else "0.00"}</div>'

    elif w_type == "Text Input":
        style += " border: 1px solid #999;"
        html = f'<input type="text" style="{style}" class="pv-input" data-pv="{pv_name}" value="{text}" title="{tooltip}">'

    elif w_type == "Action Button":
        style += " cursor: pointer; border: 1px solid #555; display: flex; align-items: center; justify-content: center;"
        html = f'<button style="{style}" class="pv-button" data-pv="{pv_name}" title="{tooltip}">{text}</button>'

    elif w_type == "Menu Button":
        html = f'<select style="{style}" data-pv="{pv_name}" title="{tooltip}"><option>{text if text else "Menu"}</option></select>'

    elif w_type == "Ellipse":
        style += " border-radius: 50%; border: 1px solid gray;"
        html = f'<div style="{style}" title="{tooltip}"></div>'
        
    elif w_type == "Rectangle":
        style += " border: 1px solid gray;"
        html = f'<div style="{style}" title="{tooltip}"></div>'
    
    elif w_type == "Grouping Container":
        style += " overflow: hidden;" # Often containers crop content
        html = f'<div style="{style}">'
        for child in widget.findall("widget"):
            html += convert_widget(child, 0, 0) # Relative to container? XML usually has absolute coords within container? 
            # In OPI, coords are relative to parent.
            # So if I use absolute positioning for everything, I need to account for parent offset if I treat the container as a relative parent.
            # BUT: CSS absolute inside a relative parent works.
            # Let's clean up style for container to be relative? No, OPI coords are usually relative to parent.
            # So if the container is at (100, 100) and child is at (10, 10), the child is at (110, 110) on screen.
            # In HTML: if container is `position: absolute; left: 100; top: 100`, then child `position: absolute; left: 10; top: 10` inside it puts it at (110, 110).
            # So I don't need to add parent_x/y recursively if I nest the divs.
        html += '</div>'
        
    else:
        # Generic fallback
        style += " border: 1px dashed red;"
        html = f'<div style="{style}" title="{w_type}:{tooltip}">{w_type}</div>'

    return html

def convert_opi_to_html(opi_path, html_path):
    tree = ET.parse(opi_path)
    root = tree.getroot()
    
    # Root display properties
    width_node = root.find("width")
    width = width_node.text if width_node is not None and width_node.text else "800"
    height_node = root.find("height")
    height = height_node.text if height_node is not None and height_node.text else "600"
    bg_color = parse_color(root.find("background_color"))
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OPI Web View: {os.path.basename(opi_path)}</title>
    <style>
        body {{
            background-color: #f0f0f0;
            font-family: sans-serif;
            margin: 0;
            padding: 20px;
        }}
        #opi-display {{
            position: relative;
            width: {width}px;
            height: {height}px;
            background-color: {bg_color};
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            margin: auto;
        }}
        .pv-readback {{ background-color: #eee; }}
        .pv-input {{ background-color: white; }}
    </style>
</head>
<body>
    <h1>OPI Web View: {os.path.basename(opi_path)}</h1>
    <div id="opi-display">
"""

    # Recursively process widgets
    # In OPI XML, widgets are children of the root <display> or nested <widget typeId="...groupingContainer">
    # The root has <widget> tags directly.
    
    for widget in root.findall("widget"):
        html_content += convert_widget(widget)
        
    html_content += """
    </div>
    <script>
        // Simple mock behavior
        document.querySelectorAll('.pv-button').forEach(btn => {
            btn.addEventListener('click', () => {
                alert('Button clicked! PV: ' + btn.getAttribute('data-pv'));
            });
        });
        
        // Mock update loop (optional)
        setInterval(() => {
            document.querySelectorAll('.pv-readback').forEach(el => {
                // Determine if it looks numeric
                let text = el.innerText;
                if (!isNaN(parseFloat(text))) {
                    // Random wiggle for demo
                    // el.innerText = (parseFloat(text) + (Math.random() - 0.5)).toFixed(2);
                }
            });
        }, 1000);
    </script>
</body>
</html>
"""
    
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"Successfully created {html_path}")

if __name__ == "__main__":
    opi_file = "/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/opi/motorx_all.opi"
    html_file = "/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/opi/motorx_all.html"
    convert_opi_to_html(opi_file, html_file)
