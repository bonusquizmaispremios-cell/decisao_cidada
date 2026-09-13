import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="DECISÃO CIDADÃ", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_cidada():
    return {"perfis": {}}

_cache = get_cache_cidada()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = ['usuario', 'historico_consultas', 'consultas_salvas', 'checklist_voto']

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_consulta(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_consultas.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_consultas': [], 'consultas_salvas': [], 'checklist_voto': {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO DE NEUTRALIDADE — compartilhado em todo prompt ---
PRINCIPIO_NEUTRALIDADE = """
PRINCÍPIO OBRIGATÓRIO DE NEUTRALIDADE — siga isso em TODA resposta:
- Você NUNCA recomenda em quem votar, qual partido apoiar, ou qual posição política "correta" adotar
- Para qualquer tema com mais de uma perspectiva legítima, APRESENTE SEMPRE pelo menos duas visões diferentes,
  de forma equilibrada, sem indicar qual é "melhor" ou "certa"
- Use linguagem de mecanismo, não de julgamento: explique COMO algo funciona e QUAIS são os argumentos de cada lado,
  nunca afirme qual argumento é mais válido
- Não tome posição sobre temas controversos atuais — apresente o debate, não vença o debate
- Trate conceitos técnicos (economia, direito constitucional, funcionamento do governo) de forma factual e didática —
  isso não é opinião, é mecanismo institucional
- Você não tem acesso a notícias em tempo real nem a dados eleitorais atualizados — não invente nomes de políticos,
  resultados de eleições ou status de projetos de lei específicos
- Se a pessoa pedir uma opinião direta sobre qual posição é "certa", explique educadamente que seu papel é ajudar
  a entender os argumentos de cada lado, não dizer qual escolher
- Português do Brasil, tom didático e respeitoso
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> este conteúdo é educativo e busca apresentar múltiplas perspectivas de forma equilibrada —
não representa uma posição política do app nem indica como você deve pensar ou votar. A IA não tem acesso a dados em
tempo real, então para fatos atuais específicos (propostas em tramitação, resultados eleitorais, etc), consulte fontes
oficiais e atualizadas.
</div>
"""

# --- MOTOR DE IA ---
def cidada_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um consultor de educação cívica, especializado em explicar política, economia e
funcionamento do governo de forma clara e imparcial.
Usuário: {st.session_state.usuario}.
{PRINCIPIO_NEUTRALIDADE}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_consultas)
    salvos = len(st.session_state.consultas_salvas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F0FDFA;border:1px solid #0D9488;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} consultas geradas · {salvos} salvas</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"decisao_cidada_{nome_usuario}.json", mime="application/json", use_container_width=True, key="decisaoc4")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# --- PARSER E RENDERIZADOR DA ANÁLISE CRÍTICA ENRIQUECIDA ---
def _extrair_secao(texto: str, marcador: str) -> str:
    """Extrai o conteúdo entre ###MARCADOR### e o próximo ### ou fim do texto."""
    padrao = rf'###{marcador}###\s*(.*?)(?=###|\Z)'
    m = re.search(padrao, texto, re.DOTALL)
    return m.group(1).strip() if m else ""

def renderizar_analise_critica(texto: str):

    # ── TABELA DE AFIRMAÇÕES ──
    sec_tabela = _extrair_secao(texto, "TABELA_AFIRMACOES")
    linhas_tabela = [l.strip() for l in sec_tabela.split('\n') if '|' in l]

    st.markdown("### 📋 Classificação das afirmações")
    if linhas_tabela:
        cores_tipo = {
            "Promessa": "#1D4ED8", "Objetivo político": "#8B5CF6", "Meta condicionada": "#B45309",
            "Princípio administrativo": "#6B7280", "Opinião": "#EC4899", "Fato verificável": "#059669",
            "Depende de terceiros": "#DC2626",
        }
        linhas_html = ""
        for linha in linhas_tabela:
            partes = [p.strip() for p in linha.split('|')]
            if len(partes) >= 2:
                afirm, tipo = partes[0], partes[1]
                cor = cores_tipo.get(tipo, "#0D9488")
                linhas_html += f"""<tr>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">{afirm}</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;"><span style="background:{cor};color:white;padding:3px 10px;border-radius:12px;font-size:0.82em;">{tipo}</span></td>
                </tr>"""
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:white;border-radius:10px;overflow:hidden;border:1px solid #E5E7EB;">
        <tr style="background:#F0FDFA;"><th style="padding:8px 12px;text-align:left;">Afirmação</th><th style="padding:8px 12px;text-align:left;">Tipo</th></tr>
        {linhas_html}
        </table>
        """, unsafe_allow_html=True)


    # ── GRAU DE OBJETIVIDADE (estrelas) ──
    sec_obj = _extrair_secao(texto, "GRAU_OBJETIVIDADE")
    def _pega_valor(secao, chave, default=0):
        m = re.search(rf'{chave}:\s*(\d+(?:[.,]\d+)?)', secao)
        if not m:
            return default
        valor_str = m.group(1).replace(',', '.')
        valor_float = float(valor_str)
        # Retorna int quando o valor é inteiro, float (1 decimal) quando tem casas decimais
        return round(valor_float) if valor_float == int(valor_float) else round(valor_float, 1)
    def _pega_texto(secao, chave):
        m = re.search(rf'{chave}:\s*(.+)', secao)
        return m.group(1).strip() if m else ""

    muito_esp = int(round(_pega_valor(sec_obj, "muito_especifico")))
    mod_esp = int(round(_pega_valor(sec_obj, "moderadamente_especifico")))
    generico = int(round(_pega_valor(sec_obj, "generico")))
    # Limita entre 0 e 5 — proteção contra valores fora da escala
    muito_esp, mod_esp, generico = max(0,min(5,muito_esp)), max(0,min(5,mod_esp)), max(0,min(5,generico))
    justificativa_obj = _pega_texto(sec_obj, "justificativa")

    def _estrelas(n, total=5):
        return "⭐" * n + "☆" * (total - n)

    st.markdown("### 📊 Grau de objetividade")
    col_o1, col_o2, col_o3 = st.columns(3)
    col_o1.markdown(f"<div class='card' style='text-align:center;padding:14px;'><div style='font-size:0.8em;color:#666;'>Muito específico</div><div style='font-size:1.3em;'>{_estrelas(muito_esp)}</div></div>", unsafe_allow_html=True)
    col_o2.markdown(f"<div class='card' style='text-align:center;padding:14px;'><div style='font-size:0.8em;color:#666;'>Moderadamente específico</div><div style='font-size:1.3em;'>{_estrelas(mod_esp)}</div></div>", unsafe_allow_html=True)
    col_o3.markdown(f"<div class='card' style='text-align:center;padding:14px;'><div style='font-size:0.8em;color:#666;'>Genérico</div><div style='font-size:1.3em;'>{_estrelas(generico)}</div></div>", unsafe_allow_html=True)
    if justificativa_obj:
        st.markdown(f"<div class='card-orange'><strong>Justificativa:</strong><br>{justificativa_obj}</div>", unsafe_allow_html=True)


    # ── TÉCNICAS DE PERSUASÃO ──
    sec_tec = _extrair_secao(texto, "TECNICAS_PERSUASAO")
    linhas_tec = [l.strip() for l in sec_tec.split('\n') if l.strip()]
    st.markdown("### 🎭 Técnicas de persuasão")
    tec_html = ""
    for linha in linhas_tec:
        if linha.upper().startswith("SIM:"):
            tec_html += f"<div class='checklist-item'>✅ {linha[4:].strip()}</div>"
        elif linha.upper().startswith("NAO:") or linha.upper().startswith("NÃO:"):
            tec_html += f"<div class='checklist-item' style='opacity:0.5;'>⬜ {linha[4:].strip()}</div>"
    if tec_html:
        st.markdown(tec_html, unsafe_allow_html=True)


    # ── O QUE FALTA PARA AVALIAR ──
    sec_falta = _extrair_secao(texto, "FALTA_PARA_AVALIAR")
    perguntas_falta = [l.strip().lstrip('-•').strip() for l in sec_falta.split('\n') if l.strip()]
    if perguntas_falta:
        st.markdown("### 📈 O que falta para avaliar melhor")
        st.markdown("<div class='card'>" + "<br>".join(f"• {p}" for p in perguntas_falta) + "</div>", unsafe_allow_html=True)

    # ── BENEFÍCIOS E DESAFIOS — lado a lado ──
    sec_benef = _extrair_secao(texto, "BENEFICIOS_POTENCIAIS")
    sec_desaf = _extrair_secao(texto, "DESAFIOS_POTENCIAIS")
    benef_linhas = [l.strip() for l in sec_benef.split('\n') if l.strip()]
    desaf_linhas = [l.strip() for l in sec_desaf.split('\n') if l.strip()]

    col_b, col_d = st.columns(2)
    with col_b:
        st.markdown("#### ⚖️ Possíveis benefícios")
        if benef_linhas:
            st.markdown("<div class='card-blue'>" + "<br>".join(benef_linhas) + "</div>", unsafe_allow_html=True)
    with col_d:
        st.markdown("#### ⚠️ Possíveis desafios")
        if desaf_linhas:
            st.markdown("<div class='card-orange'>" + "<br>".join(desaf_linhas) + "</div>", unsafe_allow_html=True)


    # ── VERIFICABILIDADE (barras) ──
    sec_verif = _extrair_secao(texto, "VERIFICABILIDADE")
    pode_medir = _pega_valor(sec_verif, "pode_ser_medido")
    tem_metas = _pega_valor(sec_verif, "tem_metas")
    tem_prazo = _pega_valor(sec_verif, "tem_prazo")
    tem_numeros = _pega_valor(sec_verif, "tem_numeros")

    st.markdown("### 🔍 Grau de verificabilidade")
    for label, valor in [("Pode ser medido?", pode_medir), ("Tem metas?", tem_metas), ("Tem prazo?", tem_prazo), ("Tem números?", tem_numeros)]:
        cor = "#059669" if valor >= 60 else ("#B45309" if valor >= 30 else "#B91C1C")
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;font-size:0.85em;font-weight:600;"><span>{label}</span><span>{valor}%</span></div>
            <div style="background:#E2E8F0;border-radius:999px;height:10px;overflow:hidden;"><div style="height:100%;border-radius:999px;background:{cor};width:{valor}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)


    # ── VIÉS EMOCIONAL ──
    sec_vies = _extrair_secao(texto, "VIES_EMOCIONAL")
    linhas_vies = [l.strip() for l in sec_vies.split('\n') if l.strip()]
    st.markdown("### 🧠 Viés emocional")
    cores_intensidade = {"Alta": "🔴", "Média": "🟡", "Baixa": "🟢"}
    vies_html = ""
    for linha in linhas_vies:
        if linha.upper().startswith("NOTA:"):
            vies_html += f"<div style='font-style:italic;color:#666;margin-top:6px;'>{linha[5:].strip()}</div>"
        elif ':' in linha:
            emocao, intensidade = linha.split(':', 1)
            emocao, intensidade = emocao.strip(), intensidade.strip()
            icone = cores_intensidade.get(intensidade, "⚪")
            vies_html += f"<span class='badge' style='background:#0D9488;'>{icone} {emocao} ({intensidade})</span> "
    if vies_html:
        st.markdown(f"<div class='card'>{vies_html}</div>", unsafe_allow_html=True)


    # ── PERGUNTAS JORNALÍSTICAS ──
    sec_perg = _extrair_secao(texto, "PERGUNTAS_JORNALISTICAS")
    perguntas_jorn = [l.strip().lstrip('-•').strip() for l in sec_perg.split('\n') if l.strip()]
    if perguntas_jorn:
        st.markdown("### 🎯 Perguntas inteligentes sobre este texto")
        st.markdown("<div class='card-dark'>" + "<br><br>".join(f"❓ {p}" for p in perguntas_jorn) + "</div>", unsafe_allow_html=True)

    # ── CONCEITOS CITADOS ──
    sec_conceitos = _extrair_secao(texto, "CONCEITOS_CITADOS")
    linhas_conceitos = [l.strip() for l in sec_conceitos.split('\n') if '|' in l]
    if linhas_conceitos:
        st.markdown("### 📚 Conceitos citados")
        for linha in linhas_conceitos:
            partes = [p.strip() for p in linha.split('|')]
            if len(partes) >= 2:
                st.markdown(f"<div class='checklist-item'>📖 <strong>{partes[0]}</strong> — {partes[1]}</div>", unsafe_allow_html=True)


    # ── NOTAS FINAIS ──
    sec_notas = _extrair_secao(texto, "NOTAS_FINAIS")
    clareza = _pega_valor(sec_notas, "clareza")
    especificidade = _pega_valor(sec_notas, "especificidade")
    detalhamento = _pega_valor(sec_notas, "detalhamento")
    verificabilidade = _pega_valor(sec_notas, "verificabilidade")
    viabilidade_txt = _pega_texto(sec_notas, "viabilidade")

    st.markdown("### ⭐ Notas Finais")
    c1, c2, c3, c4 = st.columns(4)
    for col, label, val in zip([c1,c2,c3,c4], ["Clareza","Especificidade","Detalhamento","Verificabilidade"], [clareza, especificidade, detalhamento, verificabilidade]):
        cor = "#059669" if val >= 7 else ("#B45309" if val >= 4 else "#B91C1C")
        col.markdown(f"<div class='stat-box'><div class='stat-numero' style='color:{cor} !important;'>{val}/10</div><div>{label}</div></div>", unsafe_allow_html=True)
    if viabilidade_txt:
        st.markdown(f"<div class='card' style='margin-top:10px;'>🎯 <strong>Viabilidade:</strong> {viabilidade_txt}</div>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'checklist_voto' not in st.session_state: st.session_state['checklist_voto'] = None
if 'consultas_salvas' not in st.session_state: st.session_state['consultas_salvas'] = []
if 'historico_consultas' not in st.session_state: st.session_state['historico_consultas'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 DECISÃO CIDADÃ")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":


    st.markdown("""<div class="disclaimer-topo">
    ⚖️ <strong>Este app é imparcial e educativo.</strong> Sempre apresenta múltiplas perspectivas — nunca diz em quem
    votar ou qual posição é "certa".
    </div>""", unsafe_allow_html=True)


    # TABS — navegação nativa
    (_tab_Home, _tab_Analisar, _tab_Fake, _tab_Vereador, _tab_Prefeito, _tab_Deputado, _tab_Senador, _tab_Governador, _tab_Presidente, _tab_Referendum, _tab_Proposta) = st.tabs(['🏠 Painel', '🔍 Analisar', '❌ Fake News', '🏛️ Vereador', '🏙️ Prefeito', '📜 Deputado', '🎩 Senador', '🗺️ Governador', '🇧🇷 Presidente', '📋 Referendo', '💡 Proposta'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_decisaoc")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_decisaoc", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🗳️")
            st.markdown("<span class='badge'>Educação Cívica</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="decisaoc3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_consultas) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        modulos_count = {}
        for c in st.session_state.historico_consultas:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_consultas)}</div><div>Consultas geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.consultas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(modulos_count)}</div><div>Tópicos explorados</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{sum(1 for v in st.session_state.checklist_voto.values() if v)}</div><div>Itens do checklist</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'Uma democracia saudável depende de cidadãos que pensam por si mesmos — não de cidadãos que pensam igual.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "💰 Economia": "Inflação, juros, dívida pública, impostos, PIB — explicados em linguagem simples",
            "🏛️ Governo": "Como funcionam os 3 poderes e os cargos — prefeito, governador, deputado, senador...",
            "📜 Leis": "Cole uma lei ou trecho legal e receba a tradução em português simples",
            "🎓 Aprenda Política": "Pequenas aulas sobre democracia, federalismo, reforma tributária e mais",
            "🧠 Pensamento Crítico": "Identifique vieses, falácias e manipulação emocional em qualquer texto ou discurso",
            "✅ Antes de Votar": "Checklist para organizar sua pesquisa antes de decidir o voto",
            "📚 Biblioteca": "Histórico de tudo que você já consultou",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        st.header("💰 Economia em Linguagem Simples")
        st.markdown("Entenda os conceitos econômicos que aparecem no noticiário todos os dias.")

        tema_economia = st.selectbox("Escolha um tema:", key="select_tema_economia", options=[
            "Inflação", "Taxa de juros (Selic)", "Dívida pública", "Impostos e tributos",
            "Gastos públicos", "Orçamento público (PLOA)", "PIB", "Câmbio (dólar)",
            "Reforma tributária", "Teto de gastos", "Outro (perguntar)",
        ])
        pergunta_economia = ""
        if tema_economia == "Outro (perguntar)":
            pergunta_economia = st.text_input("O que você quer entender?", placeholder="ex: O que é superávit primário?", key="input_pergunta_economia")

        if st.button("💰 EXPLICAR ESSE TEMA", key="decisaoc4_d2"):
            topico = pergunta_economia if tema_economia == "Outro (perguntar)" and pergunta_economia.strip() else tema_economia
            if topico.strip():
                with st.spinner("Preparando explicação..."):
                    prompt = (
                        f"Explique de forma simples e didática o conceito econômico: {topico}\n\n"
                        f"FORMATO:\n\n"
                        f"💰 {topico.upper()}\n\n"
                        f"📖 O QUE É (em linguagem simples):\n[explicação clara, com analogia do dia a dia se possível]\n\n"
                        f"🔍 COMO ISSO AFETA SEU BOLSO:\n[impacto prático na vida das pessoas]\n\n"
                        f"📊 COMO É MEDIDO/DECIDIDO:\n[quem calcula ou decide isso, brevemente]\n\n"
                        f"⚖️ DIFERENTES VISÕES SOBRE O TEMA:\n[se houver debate econômico legítimo sobre esse tema, apresente as principais correntes de pensamento de forma equilibrada]\n\n"
                        f"❓ PERGUNTA FREQUENTE SOBRE O TEMA:\n[1 pergunta comum + resposta]"
                    )
                    res = cidada_ia(prompt)
                    if res: st.session_state['res_home_decisa1'] = str(res)
                    salvar_consulta("Economia", topico, res)
                    st.session_state['economia_temp'] = res
            else:
                st.warning("Escolha ou descreva o tema.")

        if st.session_state.get('economia_temp'):
            st.markdown(f"<div class='card'>{st.session_state['economia_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['economia_temp'], file_name="economia.txt", mime="text/plain", use_container_width=True, key="decisaoc5")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_eco", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Economia','tema':topico if 'topico' in dir() else '','conteudo':st.session_state['economia_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # COMO FUNCIONA O GOVERNO
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
            st.download_button("💾 Salvar dados (.json)",
                data=_json_sv.dumps(_dados_sv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_sv_decisaoc")
        with _csl2:
            _arq_sv = st.file_uploader("📂 Carregar dados:", type=["json"], key="ul_sv_decisaoc")
            if _arq_sv:
                try:
                    import json as _json_ld
                    for _k, _v in _json_ld.loads(_arq_sv.read().decode()).items():
                        st.session_state[_k] = _v
                    st.success("✅ Dados carregados!")
                    st.rerun()
                except: st.error("Arquivo inválido.")

    with _tab_Analisar:
        st.header("🔍 Analisar Candidato/Proposta")
        st.markdown("*Analise qualquer candidato ou proposta política.*")
        _prompt_analisar = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_analisar_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_analisar_btn", use_container_width=True):
            if _prompt_analisar.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_analisar}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Fake:
        st.header("❌ Verificar Fake News")
        st.markdown("*Verifique se uma notícia política é verdadeira.*")
        _prompt_fake = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_fake_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_fake_btn", use_container_width=True):
            if _prompt_fake.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_fake}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Vereador:
        st.header("🏛️ Vereador")
        st.markdown("*Entenda o papel e como avaliar vereadores.*")
        _prompt_vereador = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_vereador_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_vereador_btn", use_container_width=True):
            if _prompt_vereador.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_vereador}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Prefeito:
        st.header("🏙️ Prefeito")
        st.markdown("*Entenda o papel e como avaliar prefeitos.*")
        _prompt_prefeito = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_prefeito_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_prefeito_btn", use_container_width=True):
            if _prompt_prefeito.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_prefeito}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Deputado:
        st.header("📜 Deputado")
        st.markdown("*Federal ou estadual — entenda o mandato.*")
        _prompt_deputado = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_deputado_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_deputado_btn", use_container_width=True):
            if _prompt_deputado.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_deputado}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Senador:
        st.header("🎩 Senador")
        st.markdown("*Entenda o papel do senador e como avaliá-lo.*")
        _prompt_senador = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_senador_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_senador_btn", use_container_width=True):
            if _prompt_senador.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_senador}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Governador:
        st.header("🗺️ Governador")
        st.markdown("*Entenda o papel e como avaliar governadores.*")
        _prompt_governador = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_governador_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_governador_btn", use_container_width=True):
            if _prompt_governador.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_governador}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Presidente:
        st.header("🇧🇷 Presidente")
        st.markdown("*Entenda as funções presidenciais e avalie propostas.*")
        _prompt_presidente = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_presidente_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_presidente_btn", use_container_width=True):
            if _prompt_presidente.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_presidente}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Referendum:
        st.header("📋 Referendo/Plebiscito")
        st.markdown("*Entenda como funcionam referendos e plebiscitos.*")
        _prompt_referendum = st.text_area("Descreva sua situação ou dúvida:", height=120, key="decisa_referendum_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="decisa_referendum_btn", use_container_width=True):
            if _prompt_referendum.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_referendum}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Proposta:
        pass

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Decisão Cidadã — Consultor de Educação Cívica com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
