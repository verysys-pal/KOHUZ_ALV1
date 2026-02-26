import re

def generate_dashboard():
    with open('motorx_all.html', 'r', encoding='utf-8') as f:
        m_html = f.read()
    with open('motor_popup.html', 'r', encoding='utf-8') as f:
        p_html = f.read()

    # Extract styles from motorx_all.html
    style_match = re.search(r'<style>(.*?)</style>', m_html, re.DOTALL)
    styles = style_match.group(1) if style_match else ""
    
    # Extract the <main> block for the modal content
    main_match = re.search(r'<main[^>]*>(.*?)</main>', p_html, re.DOTALL)
    modal_content = main_match.group(1) if main_match else ""

    # Replace $(P)$(M) with data-suffix logic or just keep $(P)$(M) and let JS replace it dynamically
    # For a modal that changes context, it's easier to use a placeholder like {PREFIX}
    # and when Opening the modal, we update all elements. Let's use `data-suffix`
    # Replace data-pv="$(P)$(M).NAME" with data-base-pv="true" data-suffix=".NAME"
    # Wait, the easier way is: leave the template exactly with $(P)$(M), 
    # but initially set it to a template string. Let's use `data-tpl-pv="$(P)$(M).NAME"`

    modal_content = modal_content.replace('data-pv="$(P)$(M)', 'data-tpl-pv="')
    modal_content = modal_content.replace('data-led-pv="$(P)$(M)', 'data-tpl-led-pv="')
    modal_content = modal_content.replace('data-tooltip-pv="$(P)$(M)', 'data-tpl-tooltip-pv="')
    
    # Also replace onclick="app.write('$(P)$(M).STOP', 1)"
    # with onclick="app.writePrefix('.STOP', 1)" or similar
    modal_content = modal_content.replace("app.write('$(P)$(M)", "app.writePrefix('")
    modal_content = modal_content.replace("app.writeInput('$(P)$(M)", "app.writeInputPrefix('")

    # For data-pv="$(P)allstop.VAL", just keep it or replace $(P) with prefix
    modal_content = modal_content.replace("app.write('$(P)allstop.VAL'", "app.writePrefix('allstop.VAL'")

    dashboard_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>6-Axis Motor Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        {styles}
        /* Dashboard specific */
        .axis-card {{
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }}
        .axis-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #3b82f6;
        }}
        .modal-overlay {{
            background-color: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(4px);
        }}
        .disconnected-card {{
            opacity: 0.6;
            filter: grayscale(1);
            position: relative;
        }}
        .disconnected-card::after {{
            content: "DISCONNECTED";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-15deg);
            font-weight: 900;
            font-size: 1.5rem;
            color: rgba(239, 68, 68, 0.4);
            border: 4px solid rgba(239, 68, 68, 0.3);
            padding: 0.5rem 1rem;
            pointer-events: none;
            z-index: 10;
            letter-spacing: 0.1em;
        }}
        .disconnected-card .card-body {{
            pointer-events: none;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col bg-slate-900 text-slate-200">

    <!-- Header -->
    <header class="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
        <div class="px-4 py-3 flex flex-row justify-between items-center gap-2 md:gap-4">
            <div class="flex items-center gap-2">
                <div class="bg-blue-600 p-1.5 md:p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                </div>
                <h1 class="text-sm md:text-xl font-bold text-white tracking-tight">Kohzu 6-Axis Dashboard</h1>
            </div>
            
            <div class="flex flex-row items-center gap-4">
                <div id="conn-status" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-700 text-slate-300 text-xs font-semibold">
                    <div class="w-2 h-2 rounded-full bg-red-500"></div>Disconnected
                </div>
                <button onclick="app.write('KOHZU:allstop.VAL', 1)" class="btn btn-danger flex items-center gap-1.5 shadow-lg shadow-red-900/20 text-sm py-1.5 px-4 rounded-lg font-bold">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
                    </svg>
                    ABORT ALL
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content: 6 Axes Grid -->
    <main class="flex-1 p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="axes-container">
            <!-- Populated by JS -->
        </div>
    </main>

    <!-- Detailed Control Modal -->
    <div id="detail-modal" class="hidden fixed inset-0 z-[100] modal-overlay overflow-y-auto flex justify-center items-start pt-10 pb-10">
        <div class="bg-slate-900 rounded-xl border border-slate-700 w-full max-w-7xl relative shadow-2xl flex flex-col mx-4">
            
            <!-- Modal Header -->
            <div class="flex justify-between items-center p-4 border-b border-slate-700 bg-slate-800 rounded-t-xl sticky top-0 z-10">
                <h2 class="text-xl font-bold text-white flex items-center gap-2">
                    <span id="modal-axis-title" class="text-blue-400">Axis</span>
                    <span class="text-slate-500 text-sm font-normal">Detailed Control</span>
                    <span id="modal-model-badge" class="ml-4 px-2 py-0.5 rounded text-xs bg-slate-700 text-slate-300 hidden"></span>
                </h2>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white transition-colors bg-slate-700 hover:bg-slate-600 rounded-full p-1 border border-slate-600 shadow-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            
            <!-- Modal Body ( motorx_all.html main content ) -->
            <div class="p-6 grid grid-cols-1 lg:grid-cols-5 gap-6 overflow-y-auto" style="max-height: calc(100vh - 150px);">
                {modal_content}
            </div>
        </div>
    </div>

    <!-- Hidden element for tailwind parser -->
    <div class="hidden bg-green-600 text-white border-green-600 bg-red-900/50 text-red-300 border-red-800 bg-green-900/50 text-green-300 border-green-800"></div>

    <script>
        const wsHost = window.location.hostname || 'localhost';
        const wsPort = window.location.port ? window.location.port : '8888';
        const wsUrl = `ws://${{wsHost}}:${{wsPort}}/ws`;

        const axesConfig = [null, null, null, null, null, null];
        const PREFIX = 'KOHZU:';
        let currentModalAxis = null;

        // Populate Axes Grid
        function renderDashboard() {{
            const container = document.getElementById('axes-container');
            container.innerHTML = '';
            for (let i = 0; i < 6; i++) {{
                const idx = i;
                const pvPrefix = `${{PREFIX}}m${{idx + 1}}`;
                
                // Readback and status
                const modelInfo = axesConfig[idx] 
                    ? `<span class="px-2 py-0.5 rounded text-[10px] bg-blue-900/50 text-blue-300 border border-blue-800">${{axesConfig[idx].stageModel}}</span>` 
                    : `<span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-500 border border-slate-700">No Config</span>`;

                const cardHtml = `
                <div class="card axis-card flex flex-col justify-between" id="axis-card-${{idx}}" onclick="openModal(${{idx}})">
                    <div class="card-header justify-between cursor-pointer" onclick="openModal(${{idx}}); event.stopPropagation();">
                        <div class="flex items-center gap-2">
                            <span class="card-title">Motor ${{idx + 1}}</span>
                            ${{modelInfo}}
                            <div id="axis-conn-${{idx}}" class="w-2 h-2 rounded-full bg-slate-600 ml-auto shadow-sm" title="Disconnected"></div>
                        </div>
                        <div class="flex gap-2" onclick="event.stopPropagation()">
                            <label class="btn btn-secondary text-[10px] py-1 px-2 cursor-pointer mb-0">
                                Upload JSON
                                <input type="file" class="hidden" accept=".json" onchange="handleFileUpload(event, ${{idx}})">
                            </label>
                        </div>
                    </div>
                    
                    <div class="card-body cursor-pointer flex-1 flex flex-col gap-1.5 p-3">
                        
                        <!-- Header Row -->
                        <div class="grid grid-cols-[60px_1fr_1fr_30px] gap-2 items-center text-center pb-1 border-b border-slate-700/50">
                            <div class="text-[9px] font-bold text-slate-500 uppercase text-left">
                                <span class="truncate max-w-[60px] inline-block" data-pv="${{pvPrefix}}.DESC" title="Description">Desc</span>
                            </div>
                            <div class="text-[10px] font-bold text-slate-400 uppercase">User</div>
                            <div class="text-[10px] font-bold text-slate-400 uppercase">Dial</div>
                            <div class="text-[9px] font-bold text-slate-500 uppercase pr-1">Limit</div>
                        </div>

                        <!-- Hi limit -->
                        <div class="grid grid-cols-[60px_1fr_1fr_30px] gap-2 items-center">
                            <div class="text-[10px] font-semibold text-slate-400 text-right pr-1 tracking-tight">Hi limit</div>
                            <input type="number" data-pv="${{pvPrefix}}.HLM" class="w-full input-dark text-right text-xs px-1.5 py-1" onclick="event.stopPropagation()">
                            <input type="number" data-pv="${{pvPrefix}}.DHLM" class="w-full input-dark text-right text-xs px-1.5 py-1 text-slate-500" onclick="event.stopPropagation()">
                            <div class="flex justify-center">
                                <div class="led w-3 h-3" data-led-pv="${{pvPrefix}}.HLS" data-led-on="1" data-led-color="error"></div>
                            </div>
                        </div>

                        <!-- Readback -->
                        <div class="grid grid-cols-[60px_1fr_1fr_30px] gap-2 items-center">
                            <div class="text-[10px] font-bold text-green-500 text-right pr-1 tracking-tight">Readback</div>
                            <div class="bg-black border border-slate-700 rounded px-1.5 py-1 text-right flex justify-end items-center overflow-hidden">
                                <span data-pv="${{pvPrefix}}.RBV" class="pv-font text-green-400 font-bold text-[13px] leading-none tabular-nums">0.0000</span>
                            </div>
                            <div class="bg-black border border-slate-700 rounded px-1.5 py-1 text-right flex justify-end items-center overflow-hidden">
                                <span data-pv="${{pvPrefix}}.DRBV" class="pv-font text-green-400/70 font-bold text-xs leading-none tabular-nums">0.0000</span>
                            </div>
                            <div class="flex justify-center items-center">
                                <span data-pv="${{pvPrefix}}.EGU" class="text-[9px] font-bold text-slate-500 pv-font px-0.5" title="EGU">EGU</span>
                            </div>
                        </div>

                        <!-- Drive -->
                        <div class="grid grid-cols-[60px_1fr_1fr_30px] gap-2 items-center">
                            <div class="text-[10px] font-bold text-blue-400 text-right pr-1 tracking-tight">Drive</div>
                            <input type="number" data-pv="${{pvPrefix}}.VAL" class="w-full bg-slate-900 border border-blue-900/50 focus:border-blue-500 rounded text-right text-xs px-1.5 py-1 text-white font-bold outline-none transition-colors" onclick="event.stopPropagation()">
                            <input type="number" data-pv="${{pvPrefix}}.DVAL" class="w-full input-dark text-right text-xs px-1.5 py-1 text-slate-500" onclick="event.stopPropagation()">
                            <div class="flex flex-col items-center justify-center -space-y-0.5">
                                <div class="text-[7px] text-slate-400 font-bold uppercase leading-tight mb-0.5">MOVing</div>
                                <div class="led w-2.5 h-2.5" data-led-pv="${{pvPrefix}}.DMOV" data-led-on="0" data-led-color="on"></div>
                            </div>
                        </div>

                        <!-- Lo limit -->
                        <div class="grid grid-cols-[60px_1fr_1fr_30px] gap-2 items-center">
                            <div class="text-[10px] font-semibold text-slate-400 text-right pr-1 tracking-tight">Lo limit</div>
                            <input type="number" data-pv="${{pvPrefix}}.LLM" class="w-full input-dark text-right text-xs px-1.5 py-1" onclick="event.stopPropagation()">
                            <input type="number" data-pv="${{pvPrefix}}.DLLM" class="w-full input-dark text-right text-xs px-1.5 py-1 text-slate-500" onclick="event.stopPropagation()">
                            <div class="flex justify-center">
                                <div class="led w-3 h-3" data-led-pv="${{pvPrefix}}.LLS" data-led-on="1" data-led-color="error"></div>
                            </div>
                        </div>

                        <!-- Tweak -->
                        <div class="flex items-center gap-1 mt-1 pt-2 border-t border-slate-700/50">
                            <span class="text-[10px] font-semibold text-slate-400 w-[60px] text-right pr-1">Tweak</span>
                            <button onclick="app.write('${{pvPrefix}}.JOGR', 1); event.stopPropagation();" onmouseup="app.write('${{pvPrefix}}.JOGR', 0)" class="btn btn-secondary flex-1 py-1 text-[10px] font-bold border-slate-600 min-w-0 px-0">Go-</button>
                            <button onclick="app.write('${{pvPrefix}}.TWR', 1); event.stopPropagation();" class="btn btn-secondary px-2 py-1 text-xs font-bold border-slate-600">&lt;</button>
                            <input type="number" data-pv="${{pvPrefix}}.TWV" class="w-[60px] input-dark text-center text-xs px-1 py-1" onclick="event.stopPropagation()">
                            <button onclick="app.write('${{pvPrefix}}.TWF', 1); event.stopPropagation();" class="btn btn-secondary px-2 py-1 text-xs font-bold border-slate-600">&gt;</button>
                            <button onclick="app.write('${{pvPrefix}}.JOGF', 1); event.stopPropagation();" onmouseup="app.write('${{pvPrefix}}.JOGF', 0)" class="btn btn-secondary flex-1 py-1 text-[10px] font-bold border-slate-600 min-w-0 px-0">Go+</button>
                        </div>
                        
                        <!-- Status row -->
                        <div class="flex justify-between items-center mt-1 pt-1 border-t border-slate-700/50">
                            <div class="flex items-center gap-1.5">
                                <span class="truncate text-[9px] text-slate-600 bg-black px-1 rounded border border-slate-800" data-pv="${{pvPrefix}}.DTYP" title="DTYP">Type</span>
                                <div id="axis-movn-status-${{idx}}" class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-800 text-slate-500 border border-slate-700">IDLE</div>
                                <!-- Hidden subscription for MOVN -->
                                <span data-pv="${{pvPrefix}}.MOVN" class="hidden"></span>
                            </div>
                            <button onclick="app.write('${{pvPrefix}}.STOP', 1); event.stopPropagation();" class="btn btn-danger py-1 px-4 text-[10px] shadow-lg shadow-red-900/20 border border-red-500 font-bold tracking-wider rounded">STOP</button>
                        </div>
                        <!-- Hidden MSTA for hardware health monitoring -->
                        <div class="hidden" data-pv="${{pvPrefix}}.MSTA"></div>
                    </div>
                </div>
                `;
                container.innerHTML += cardHtml;
            }}
            
            // Need to re-bind elements if app is running
            if (app.ws && app.ws.readyState === WebSocket.OPEN) {{
                app.bindDOM();
            }}
        }}

        function handleFileUpload(event, axisIndex) {{
            const file = event.target.files[0];
            if (!file) return;

            // Check if motor is moving
            const pvPrefix = `${{PREFIX}}m${{axisIndex + 1}}`;
            const dmovEl = document.querySelector(`[data-led-pv="${{pvPrefix}}.DMOV"]`);
            if (dmovEl && !dmovEl.classList.contains('on')) {{
                const proceed = confirm(`Motor ${{axisIndex + 1}} appears to be moving or is disconnected (DMOV != 1).\\nAre you sure you want to apply parameters?`);
                if (!proceed) {{
                    event.target.value = '';
                    return;
                }}
            }}

            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const configData = JSON.parse(e.target.result);
                    axesConfig[axisIndex] = configData;

                    // Send EPICS parameters
                    const p = configData.parameters;
                    if(p.UREV !== undefined) app.write(`${{pvPrefix}}.UREV`, p.UREV);
                    if(p.SREV !== undefined) app.write(`${{pvPrefix}}.SREV`, p.SREV);
                    if(p.MRES !== undefined) app.write(`${{pvPrefix}}.MRES`, p.MRES);
                    if(p.VELO !== undefined) app.write(`${{pvPrefix}}.VELO`, p.VELO);
                    if(p.VMAX !== undefined) app.write(`${{pvPrefix}}.VMAX`, p.VMAX);
                    if(p.HLM !== undefined) app.write(`${{pvPrefix}}.HLM`, p.HLM);
                    if(p.LLM !== undefined) app.write(`${{pvPrefix}}.LLM`, p.LLM);
                    if(p.DHLM !== undefined) app.write(`${{pvPrefix}}.DHLM`, p.DHLM);
                    if(p.DLLM !== undefined) app.write(`${{pvPrefix}}.DLLM`, p.DLLM);
                    if(p.JVEL !== undefined) app.write(`${{pvPrefix}}.JVEL`, p.JVEL);
                    if(p.JAR !== undefined) app.write(`${{pvPrefix}}.JAR`, p.JAR);
                    if(p.PREC !== undefined) app.write(`${{pvPrefix}}.PREC`, p.PREC);
                    
                    // Also EGU, if string
                    // WebSocket can handle string writing to EPICS string records conceptually
                    // Wait, .EGU is DBF_STRING.
                    if(p.EGU !== undefined) app.write(`${{pvPrefix}}.EGU`, p.EGU);

                    alert(`Successfully applied config: ${{configData.stageModel}} to Motor ${{axisIndex + 1}}`);
                    renderDashboard();
                }} catch (err) {{
                    alert('Invalid JSON file.');
                    console.error(err);
                }}
            }};
            reader.readAsText(file);
            event.target.value = ''; // Reset
        }}

        function openModal(idx) {{
            currentModalAxis = idx;
            const pvPrefix = `${{PREFIX}}m${{idx + 1}}`;
            
            document.getElementById('modal-axis-title').innerText = `Motor ${{idx + 1}} (${{pvPrefix}})`;
            
            const badge = document.getElementById('modal-model-badge');
            if (axesConfig[idx]) {{
                badge.innerText = axesConfig[idx].stageModel;
                badge.classList.remove('hidden');
            }} else {{
                badge.classList.add('hidden');
            }}

            // Rebind Modal PVs dynamically
            const modal = document.getElementById('detail-modal');
            
            modal.querySelectorAll('[data-tpl-pv]').forEach(el => {{
                el.setAttribute('data-pv', pvPrefix + el.getAttribute('data-tpl-pv'));
            }});
            modal.querySelectorAll('[data-tpl-led-pv]').forEach(el => {{
                el.setAttribute('data-led-pv', pvPrefix + el.getAttribute('data-tpl-led-pv'));
            }});
            modal.querySelectorAll('[data-tpl-tooltip-pv]').forEach(el => {{
                el.setAttribute('data-tooltip-pv', pvPrefix + el.getAttribute('data-tpl-tooltip-pv'));
            }});

            // Render Specs and Driver Settings if present in config
            const specsList = document.getElementById('modal-specs-list');
            const driverList = document.getElementById('modal-driver-list');
            const stageBadge = document.getElementById('modal-stage-badge');
            
            if (axesConfig[idx]) {{
                stageBadge.innerText = axesConfig[idx].stageModel || "Unknown";
                
                if (axesConfig[idx].specifications) {{
                    specsList.innerHTML = Object.entries(axesConfig[idx].specifications)
                        .map(([k, v]) => `<div class="flex justify-between border-b border-slate-700/50 pb-1.5"><span class="text-slate-500 font-bold tracking-tight">${{k}}</span><span class="text-slate-200 text-right font-semibold">${{v}}</span></div>`)
                        .join('');
                }} else {{
                    specsList.innerHTML = '<div class="text-slate-600 italic text-center py-4">No specifications found</div>';
                }}
                
                if (axesConfig[idx].driverSettings) {{
                    driverList.innerHTML = Object.entries(axesConfig[idx].driverSettings)
                        .map(([k, v]) => `<div class="flex justify-between border-b border-slate-700/50 pb-1.5"><span class="text-slate-500 font-bold tracking-tight">${{k}}</span><span class="text-slate-300 text-right font-mono">${{v}}</span></div>`)
                        .join('');
                }} else {{
                    driverList.innerHTML = '<div class="text-slate-600 text-center py-2">No driver settings</div>';
                }}
            }} else {{
                stageBadge.innerText = "No Stage Selected";
                specsList.innerHTML = '<div class="text-slate-600 italic text-center py-8">Please upload a JSON configuration file to view specifications.</div>';
                driverList.innerHTML = '';
            }}

            modal.classList.remove('hidden');
            
            // Let the controller rescan and subscribe
            app.bindDOM();
        }}

        function closeModal() {{
            document.getElementById('detail-modal').classList.add('hidden');
            currentModalAxis = null;
            
            // Clean up modal bindings to prevent updates for closed modal?
            // Optionally, but WS overhead for 1 off axis isn't much.
            // But we will rebind DOM to make sure we don't have duplicated data-actua-pv mismatch 
            // Better to remove data-actual-pv from modal
            const modal = document.getElementById('detail-modal');
            modal.querySelectorAll('[data-actual-pv]').forEach(el => {{
                el.removeAttribute('data-actual-pv');
                el.removeAttribute('data-pv');
                el.removeAttribute('data-led-pv');
                el.removeAttribute('data-tooltip-pv');
            }});
        }}


        class EPICSController {{
            constructor() {{
                this.ws = null;
                this.pvs = new Set();
                this.domElements = [];
                this.init();
            }}

            init() {{
                this.ws = new WebSocket(wsUrl);
                this.ws.onopen = () => this.onOpen();
                this.ws.onmessage = (e) => this.onMessage(JSON.parse(e.data));
                this.ws.onclose = () => {{
                    this.updateStatus(false);
                    setTimeout(() => this.init(), 3000);
                }};
                this.ws.onerror = (e) => console.error(e);
            }}

            onOpen() {{
                this.updateStatus(true);
                this.bindDOM();
            }}

            bindDOM() {{
                this.pvs.clear();
                
                // Clear old tooltips
                document.querySelectorAll('.pv-tooltip').forEach(e=>e.remove());

                // Scan all PV tagged elements
                document.querySelectorAll('[data-pv], [data-led-pv], [data-tooltip-pv]').forEach(el => {{
                    // Skip if hidden inside modal and NO actual data-pv?
                    // Actually templates don't have data-pv until openModal sets them!
                    // So we can safely bind any element that matched the querySelector.
                    let resolved = el.getAttribute('data-pv') || el.getAttribute('data-led-pv') || el.getAttribute('data-tooltip-pv');
                    if (!resolved) return;

                    el.setAttribute('data-actual-pv', resolved);

                    if (el.tagName === 'INPUT' || el.tagName === 'SELECT') {{
                        el.onchange = (e) => this.write(resolved, el.type === 'number' ? parseFloat(e.target.value) : e.target.value);
                    }}

                    this.pvs.add(resolved);

                    // Re-bind tooltips
                    el.setAttribute('title', resolved); // Built-in tooltip fallback
                    if (!el.hasAttribute('data-tooltip-bound')) {{
                        el.setAttribute('data-tooltip-bound', 'true');
                        let tooltipTimeout;
                        let tooltipEl = null;

                        el.addEventListener('mouseenter', () => {{
                            tooltipTimeout = setTimeout(() => {{
                                tooltipEl = document.createElement('div');
                                tooltipEl.className = 'pv-tooltip';
                                tooltipEl.innerText = el.getAttribute('data-actual-pv');
                                el.appendChild(tooltipEl);
                                void tooltipEl.offsetWidth;
                                tooltipEl.classList.add('show');
                            }}, 1000);
                        }});

                        el.addEventListener('mouseleave', () => {{
                            clearTimeout(tooltipTimeout);
                            if (tooltipEl) {{ tooltipEl.remove(); tooltipEl = null; }}
                        }});
                    }}
                }});

                if (this.ws && this.ws.readyState === WebSocket.OPEN) {{
                    this.ws.send(JSON.stringify({{ type: 'subscribe', pvs: Array.from(this.pvs) }}));
                }}
            }}

            updateStatus(connected) {{
                const el = document.getElementById('conn-status');
                if (connected) {{
                    el.className = "flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-900/50 text-green-300 text-xs font-semibold border border-green-800";
                    el.innerHTML = '<div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>Connected';
                }} else {{
                    el.className = "flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-900/50 text-red-300 text-xs font-semibold border border-red-800";
                    el.innerHTML = '<div class="w-2 h-2 rounded-full bg-red-500"></div>Disconnected';
                }}
            }}

            onMessage(data) {{
                if (data.type === 'connection' && data.pv.endsWith('.RBV')) {{
                    const match = data.pv.match(/KOHZU:m(\\d+)/);
                    if(match) {{
                        const axisIdx = parseInt(match[1]) - 1;
                        const indicator = document.getElementById(`axis-conn-${{axisIdx}}`);
                        if(indicator) {{
                            const card = document.getElementById(`axis-card-${{axisIdx}}`);
                            if(data.connected) {{
                                // Initial connection - we don't know MSTA yet, so default to green if not grayed out
                                // But better to wait for MSTA update
                                indicator.className = "w-2 h-2 rounded-full bg-green-500 ml-auto shadow-[0_0_8px_#22c55e]";
                                indicator.title = "IOC Connected (Waiting for MSTA)";
                            }} else {{
                                indicator.className = "w-2 h-2 rounded-full bg-slate-600 ml-auto shadow-sm";
                                indicator.title = "IOC Disconnected";
                                if(card) card.classList.add('disconnected-card');
                            }}
                        }}
                    }}
                    return;
                }}

                if (data.type === 'update' && data.pv.endsWith('.MSTA')) {{
                    const match = data.pv.match(/KOHZU:m(\d+)/);
                    if(match) {{
                        const axisIdx = parseInt(match[1]) - 1;
                        const card = document.getElementById(`axis-card-${{axisIdx}}`);
                        const indicator = document.getElementById(`axis-conn-${{axisIdx}}`);
                        const isProblem = (data.value & 512) !== 0; // Bit 9: RA_PROBLEM
                        
                        if (isProblem) {{
                            if(card) card.classList.add('disconnected-card');
                            if(indicator) {{
                                indicator.className = "w-2 h-2 rounded-full bg-red-500 ml-auto shadow-[0_0_8px_#ef4444]";
                                indicator.title = "Hardware Problem / Not Connected";
                            }}
                        }} else {{
                            if(card) card.classList.remove('disconnected-card');
                            if(indicator) {{
                                indicator.className = "w-2 h-2 rounded-full bg-green-500 ml-auto shadow-[0_0_8px_#22c55e]";
                                indicator.title = "Connected";
                            }}
                        }}

                        // Update MSTA bit LEDs in modal if open
                        if (currentModalAxis === axisIdx) {{
                            document.querySelectorAll('[data-msta-bit]').forEach(el => {{
                                const bit = parseInt(el.getAttribute('data-msta-bit'));
                                if ((data.value & (1 << bit)) !== 0) {{
                                    el.classList.add('on');
                                }} else {{
                                    el.classList.remove('on');
                                }}
                            }});
                        }}
                    }}
                    return;
                }}

                if (data.type !== 'update') return;

                document.querySelectorAll(`[data-actual-pv="${{data.pv}}"]`).forEach(el => {{
                    if (el.classList.contains('led')) {{
                        const targetVal = el.getAttribute('data-led-on') || "1";
                        if (String(data.value) == targetVal) {{
                            el.classList.add(el.getAttribute('data-led-color') || 'on');
                        }} else {{
                            el.classList.remove('on', 'warn', 'error');
                        }}
                        return;
                    }}

                    if (el.tagName === 'INPUT') {{
                        if (document.activeElement !== el) el.value = data.value;
                    }} else if (el.tagName === 'SELECT') {{
                        el.value = data.value;
                    }} else {{
                        if (el.hasAttribute('data-tooltip-pv') && !el.hasAttribute('data-pv')) return;

                        let val = data.value;
                        if (typeof val === 'number') val = val.toFixed(4).replace(/\.?0+$/, '');
                        el.innerText = val;
                    }}
                }});

                // Check for dynamic overlay updates from Motor X
                if (data.pv.endsWith('.MOVN')) {{
                    const match = data.pv.match(/KOHZU:m(\d+)/);
                    if (match) {{
                        const axisIdx = parseInt(match[1]) - 1;
                        
                        // Update on main dashboard card
                        const cardMovn = document.getElementById(`axis-movn-status-${{axisIdx}}`);
                        if (cardMovn) {{
                            cardMovn.innerText = data.value ? "MOVING" : "IDLE";
                            cardMovn.className = data.value 
                                ? "px-2 py-0.5 rounded text-[9px] font-bold bg-blue-600 text-white animate-pulse" 
                                : "px-2 py-0.5 rounded text-[9px] font-bold bg-slate-800 text-slate-500 border border-slate-700";
                        }}

                        // Update in modal if open for this axis
                        if (currentModalAxis === axisIdx) {{
                            const overlay = document.getElementById('moving-overlay');
                            const statusDiv = document.getElementById('status-movn');
                            if (overlay) overlay.style.opacity = data.value ? "1" : "0";
                            if (statusDiv) {{
                                statusDiv.innerText = data.value ? "MOVING" : "IDLE";
                                statusDiv.className = data.value 
                                    ? "px-3 py-1 rounded text-xs font-bold bg-blue-600 text-white animate-pulse" 
                                    : "px-3 py-1 rounded text-xs font-bold bg-slate-700 text-slate-400";
                            }}
                        }}
                    }}
                }}
            }}

            write(pv, value) {{
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {{
                    this.ws.send(JSON.stringify({{ type: 'write', pv, value }}));
                }}
            }}

            writePrefix(suffix, value) {{
                if (currentModalAxis !== null) {{
                    const pv = `${{PREFIX}}m${{currentModalAxis + 1}}${{suffix}}`;
                    this.write(pv, value);
                }} else if (suffix.startsWith('allstop')) {{
                     // Special case: all axis stop
                     this.write(`${{PREFIX}}${{suffix}}`, value);
                }}
            }}

            writeInputPrefix(suffix) {{
                if (currentModalAxis !== null) {{
                    const pv = `${{PREFIX}}m${{currentModalAxis + 1}}${{suffix}}`;
                    const el = document.querySelector(`input[data-actual-pv="${{pv}}"]`);
                    if (el) this.write(pv, parseFloat(el.value));
                }}
            }}
        }}

        // Init UI
        const app = new EPICSController();
        renderDashboard();

        // Control mode shortcut
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Control') document.body.classList.add('debug-mode');
        }});
        document.addEventListener('keyup', (e) => {{
            if (e.key === 'Control') document.body.classList.remove('debug-mode');
        }});
    </script>
</body>
</html>
"""
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    print("Dashboard generated successfully.")

if __name__ == "__main__":
    generate_dashboard()
