import json
import re

FILE_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/PAINEL_OPERACIONAL_FUNIL_AH3.html"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ajustar os KPIs no topo
kpis_old = """      <!-- Auditados CRM -->
      <div class="bg-[#111827] border border-blue-500/30 rounded-xl p-3.5 flex flex-col justify-between">
        <span class="text-[11px] font-semibold text-blue-400 uppercase tracking-wider">Auditados CRM</span>
        <div class="flex items-baseline justify-between mt-2">
          <span class="text-2xl font-extrabold text-blue-400" id="kpi-auditados">42</span>
          <span class="text-[10px] font-medium text-blue-300 bg-blue-950/60 px-1.5 py-0.5 rounded">30 c/ WA</span>
        </div>
      </div>"""

kpis_new = """      <!-- Sem Google Maps -->
      <div class="bg-[#111827] border border-rose-500/50 rounded-xl p-3.5 flex flex-col justify-between relative overflow-hidden">
        <div class="absolute -right-4 -bottom-4 w-14 h-14 bg-rose-500/10 rounded-full blur-md"></div>
        <span class="text-[11px] font-semibold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
          🚨 Sem Maps
        </span>
        <div class="flex items-baseline justify-between mt-2">
          <span class="text-2xl font-extrabold text-rose-400" id="kpi-sem-maps">12</span>
          <span class="text-[10px] font-bold text-rose-300 bg-rose-950/80 border border-rose-800/60 px-1.5 py-0.5 rounded">Foco Instagram</span>
        </div>
      </div>"""

content = content.replace(kpis_old, kpis_new)

# Ajustar o KPI "Sem Contato" para "iFood Ativo"
kpi_sem_old = """      <!-- Sem Contato -->
      <div class="bg-[#111827] border border-rose-500/30 rounded-xl p-3.5 flex flex-col justify-between">
        <span class="text-[11px] font-semibold text-rose-400 uppercase tracking-wider">Sem Contato</span>
        <div class="flex items-baseline justify-between mt-2">
          <span class="text-2xl font-extrabold text-rose-400" id="kpi-sem">10</span>
          <span class="text-[10px] font-medium text-rose-300 bg-rose-950/60 px-1.5 py-0.5 rounded">Isolados</span>
        </div>
      </div>"""

kpi_ifood_new = """      <!-- iFood Ativo -->
      <div class="bg-[#111827] border border-red-500/30 rounded-xl p-3.5 flex flex-col justify-between">
        <span class="text-[11px] font-semibold text-red-400 uppercase tracking-wider">iFood Delivery</span>
        <div class="flex items-baseline justify-between mt-2">
          <span class="text-2xl font-extrabold text-red-400" id="kpi-ifood">92</span>
          <span class="text-[10px] font-medium text-red-300 bg-red-950/60 px-1.5 py-0.5 rounded">Taxa 12-27%</span>
        </div>
      </div>"""

content = content.replace(kpi_sem_old, kpi_ifood_new)

# 2. Atualizar a função atualizarKpis()
js_kpis_old = """    function atualizarKpis() {
      const total = LEADS.length;
      const wa = LEADS.filter(x => x.apto_wa).length;
      const auditados = LEADS.filter(x => x.status_crm === 'auditado').length;
      const fixos = LEADS.filter(x => x.canal === 'Fixo').length;
      const sem = LEADS.filter(x => x.canal === 'Sem Contato').length;
      
      const avaliacoesTotais = LEADS.reduce((acc, x) => acc + x.avaliacoes, 0);
      const notasValidas = LEADS.map(x => parseFloat(x.nota)).filter(x => !isNaN(x));
      const mediaNota = notasValidas.length ? (notasValidas.reduce((a,b)=>a+b,0) / notasValidas.length).toFixed(1) : '4.4';

      document.getElementById('kpi-total').textContent = total;
      document.getElementById('kpi-wa').textContent = wa;
      document.getElementById('kpi-auditados').textContent = auditados;
      document.getElementById('kpi-fixos').textContent = fixos;
      document.getElementById('kpi-sem').textContent = sem;
      document.getElementById('kpi-avg').textContent = mediaNota + '★';
      document.getElementById('kpi-total-rev').textContent = (avaliacoesTotais/1000).toFixed(1) + 'k rev';
    }"""

js_kpis_new = """    function atualizarKpis() {
      const total = LEADS.length;
      const wa = LEADS.filter(x => x.apto_wa).length;
      const semMaps = LEADS.filter(x => !x.tem_maps).length;
      const ifood = LEADS.filter(x => x.tem_ifood).length;
      const fixos = LEADS.filter(x => x.canal === 'Fixo').length;
      
      const avaliacoesTotais = LEADS.reduce((acc, x) => acc + x.avaliacoes, 0);
      const notasValidas = LEADS.map(x => parseFloat(x.nota)).filter(x => !isNaN(x));
      const mediaNota = notasValidas.length ? (notasValidas.reduce((a,b)=>a+b,0) / notasValidas.length).toFixed(1) : '4.4';

      document.getElementById('kpi-total').textContent = total;
      document.getElementById('kpi-wa').textContent = wa;
      if (document.getElementById('kpi-sem-maps')) document.getElementById('kpi-sem-maps').textContent = semMaps;
      if (document.getElementById('kpi-ifood')) document.getElementById('kpi-ifood').textContent = ifood;
      document.getElementById('kpi-fixos').textContent = fixos;
      document.getElementById('kpi-avg').textContent = mediaNota + '★';
      document.getElementById('kpi-total-rev').textContent = (avaliacoesTotais/1000).toFixed(1) + 'k rev';
    }"""

content = content.replace(js_kpis_old, js_kpis_new)

# 3. Atualizar renderização da tabela para incluir o botão de Instagram e badges
# Vamos ajustar a coluna do nome para mostrar [SEM MAPS] e nas ações mostrar o botão de Instagram
render_row_old = """          <td class="py-3 px-4">
            <div class="font-bold text-white text-xs hover:text-amber-400 transition-colors cursor-pointer" onclick="verDetalhes('${lead.id}')">
              ${lead.nome}
            </div>
            <div class="text-[10px] text-gray-400">${lead.categoria}</div>
          </td>"""

render_row_new = """          <td class="py-3 px-4">
            <div class="font-bold text-white text-xs hover:text-amber-400 transition-colors cursor-pointer flex items-center gap-1.5" onclick="verDetalhes('${lead.id}')">
              ${lead.nome}
              ${!lead.tem_maps ? '<span class="px-1.5 py-0.5 rounded text-[9px] font-black bg-rose-950 text-rose-400 border border-rose-800 animate-pulse">SEM MAPS</span>' : ''}
              ${lead.tem_ifood ? '<span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-red-950 text-red-400 border border-red-900">iFood</span>' : ''}
            </div>
            <div class="text-[10px] text-gray-400">${lead.categoria}</div>
          </td>"""

content = content.replace(render_row_old, render_row_new)

# 4. Inserir botão de Instagram nas ações da linha
acoes_old = """        // Ações
        let acoesHtml = '';
        if (lead.apto_wa) {
          acoesHtml = `
            <div class="flex items-center justify-end gap-1.5">
              <a href="${lead.wa_link}" target="_blank" class="px-2.5 py-1.5 bg-emerald-500/10 hover:bg-emerald-500 hover:text-black text-emerald-400 font-semibold border border-emerald-500/30 rounded-lg transition-all flex items-center gap-1.5">"""

acoes_new = """        // Ações
        let instaBtn = '';
        if (!lead.tem_maps) {
          instaBtn = `<a href="${lead.link_instagram}" target="_blank" title="Pesquisar Instagram (Melhor canal)" class="px-2 py-1.5 bg-rose-500/10 hover:bg-rose-500 hover:text-white text-rose-400 font-semibold border border-rose-500/30 rounded-lg transition-all flex items-center gap-1 text-[11px]">📸 Instagram</a>`;
        }

        let acoesHtml = '';
        if (lead.apto_wa) {
          acoesHtml = `
            <div class="flex items-center justify-end gap-1.5">
              ${instaBtn}
              <a href="${lead.wa_link}" target="_blank" class="px-2.5 py-1.5 bg-emerald-500/10 hover:bg-emerald-500 hover:text-black text-emerald-400 font-semibold border border-emerald-500/30 rounded-lg transition-all flex items-center gap-1.5">"""

content = content.replace(acoes_old, acoes_new)

# 5. Ajustar o modal para exibir alerta de Instagram quando sem_maps
modal_obs_old = "document.getElementById('m-obs').textContent = lead.observacoes || 'Sem observações adicionais.';"
modal_obs_new = """      if (!lead.tem_maps) {
        document.getElementById('m-obs').innerHTML = `<div class="p-3 mb-2 bg-rose-950/60 border border-rose-800 rounded-lg text-rose-200">
          <div class="font-bold text-rose-400 text-xs mb-1">🚨 SEM GOOGLE MAPS — MELHOR CANAL É O INSTAGRAM</div>
          <div class="text-[11px] mb-2">Este restaurante não está no Google Maps. A prospecção recomendada é acessar o Instagram para capturar o WhatsApp do gestor.</div>
          <a href="${lead.link_instagram}" target="_blank" class="inline-flex items-center gap-1 px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded text-xs transition-colors">
            📸 Abrir Perfil no Instagram
          </a>
        </div>` + (lead.observacoes || '');
      } else {
        document.getElementById('m-obs').textContent = lead.observacoes || 'Sem observações adicionais.';
      }"""

content = content.replace(modal_obs_old, modal_obs_new)

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Painel Operacional 100% refinado e salvo!")
